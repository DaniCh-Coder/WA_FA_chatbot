# wa_services.py
"""
Este módulo contiene se encarga de manejar la API con WhatsApp.
Contiene la lógica para enviar mensajes de texto y botones interactivos a través de la API de WhatsApp Business.
Además, contiene la lógica para procesar solicitudes POST de webhook de WhatsApp Business API.
"""

import logging
import json
from fastapi import HTTPException
from app.config_setup.settings import settings
from app.schemas.webhook_schema import WebhookPayload
from app.config_setup.config_settings import get_settings
from typing import Dict, Any
import httpx

# Menú de opciones
MENU_BUTTONS = [
    {"type": "reply", "reply": {"id": "pileta", "title": "Pileta"}},
    {"type": "reply", "reply": {"id": "tenis", "title": "Tenis"}},
    {"type": "reply", "reply": {"id": "sum", "title": "SUM"}}
]

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.settings = get_settings()
        self.headers = {
            "Authorization": f"Bearer {self.settings.ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        self.base_url = (
            f"{self.settings.META_URL}/"
            f"{self.settings.META_API_VER}/"
            f"{self.settings.PHONE_NUMBER_ID}/messages"
        )

    def re_format_number(self, from_number: str) -> str:
        """
        Verifica si el número de teléfono del remitente es el número de teléfono de WhatsApp Business API.
        Si es así, cambia el FORMATO del número de teléfono del remitente al número de teléfono de WhatsApp Business API.
        """
        if from_number == settings.RECIPIENT_WAID_1:
            from_number = settings.RECIPIENT_ITEM_1
            logger.info(f"RECIPIENT_WAID_1: {settings.RECIPIENT_WAID_1} detectado, cambiando a RECIPIENT_ITEM_1: {settings.RECIPIENT_ITEM_1}")
        else:
            logger.info(f"RECIPIENT_WAID_1: {settings.RECIPIENT_WAID_1} no detectado.")
        return from_number        

    async def send_message(self, payload: Dict[str, Any]) -> Dict:
        """
        Envía una solicitud POST a la API de WhatsApp Business.

        Args:
            payload (Dict[str, Any]): Cuerpo del mensaje a enviar.

        Returns:
            Dict: Respuesta de la API de WhatsApp Business.
        """
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Enviando mensaje con payload: {json.dumps(payload, indent=2)}")
                response = await client.post(
                    self.base_url, headers=self.headers, json=payload
                )
                response.raise_for_status()
                logger.info("Mensaje enviado exitosamente.")
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"Error HTTP al enviar el mensaje: {e.response.status_code} - {e.response.text}"
                )
                raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
            except httpx.RequestError as e:
                logger.error(f"Error de conexión o inesperado: {str(e)}")
                raise HTTPException(status_code=500, detail="Error al enviar el mensaje")

    async def send_text_message_to_user(self, phone_number: str, text: str) -> Dict:
        """
        Envía un mensaje de texto simple.

        Args:
            phone_number (str): Número de teléfono del destinatario.
            text (str): Texto del mensaje.

        Returns:
            Dict: Respuesta de la API de WhatsApp Business.
        """
        logger.info(f"Control del formato del número de teléfono del remitente: {phone_number}")
        phone_number = self.re_format_number(phone_number)
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": text},
        }
        return await self.send_message(payload)

    async def send_interactive_buttons(self, phone_number: str, body_text: str, buttons: list) -> Dict:
        """
        Envía botones interactivos.

        Args:
            phone_number (str): Número de teléfono del destinatario.
            body_text (str): Texto del cuerpo del mensaje.
            buttons (list): Lista de botones interactivos.

        Returns:
            Dict: Respuesta de la API de WhatsApp Business.
        """
        phone_number = self.re_format_number(phone_number)
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": buttons},
            },
        }
        return await self.send_message(payload)
    


async def handle_webhook_POST_logic(payload: WebhookPayload) -> dict:
    """
    Maneja la lógica principal para procesar solicitudes POST de webhook.

    Args:
        request (Request): Solicitud entrante.
        payload (WebhookPayload): Datos del webhook.

    Returns:
        dict: Respuesta de estado.
    """
    # Instanciar el servicio de WhatsApp
    wa_service = WhatsAppService()
    
    # Validar el payload
    if payload.validate_payload() == { "success": True }:
        logger.info(f"Payload validado exitosamente.")
    else:
        logger.error(f"Error al validar el payload: {payload}")
        raise HTTPException(status_code=400, detail="Error al validar el payload")
    
    # Iterar sobre cada entry
    for entry in payload.entry:
        account_id = entry['id']  # ID de la cuenta
        logger.info(f"Procesando eventos para la cuenta: {account_id}")
        
        # Iterar sobre los cambios dentro de cada entry
        for change in entry['changes']:
            value = change['value']
            
            # Verificar si hay mensajes
            if 'messages' in value:
                for message in value['messages']:
                    from_number = message['from']
                    message_id = message['id']
                    match message['type']:
                        case 'text':                        
                            message_body = message['text']['body']
                            
                            # Procesar cada mensaje individualmente
                            logger.info(f"Mensaje tipo texto recibido: - ID: {message_id}  - De (from_number): {from_number}  - Contenido (text:body): {message_body}")

                            # Responder al mensaje del remitente
                            response1 = await wa_service.send_text_message_to_user(from_number, "Hola!")
                            response2=  await wa_service.send_interactive_buttons(from_number, "Por favor, elije una opción:", MENU_BUTTONS)
                            logger.info(f"Respuesta enviada: \n{response1}.\n{response2}")
                        
                        case 'interactive':
                            interactive_type = message['interactive']['type']
                            match interactive_type:
                                case 'button_reply':
                                    button_id = message['interactive']['button_reply']['id']
                                    button_title = message['interactive']['button_reply']['title']
                                    logger.info(f"Botón interactivo presionado: {button_id, button_title}")
                                case 'list_reply':
                                    button_id = message['interactive']['list_reply']['id']
                                    button_title = message['interactive']['list_reply']['title']
                                    logger.info(f"Botón interactivo presionado: {button_id, button_title}")                       
                        case _: 
                            logger.info(f"Mensaje no procesado: {message}")
                            
                            
            # Verificar si hay estados
            if 'statuses' in value:
                for status in value['statuses']:
                    message_id = status['id']
                    status = status['status']
                    logger.info(f"  Estado del mensaje id.{message_id}: {status}")
                                        
    return {
        "status": "success",
        "description": "Mensaje procesado exitosamente.",
    }
