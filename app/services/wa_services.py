# wa_services.py
"""
Este módulo contiene funciones para enviar mensajes de WhatsApp Business API.
..........................................................................
"""
"""
Este módulo contiene funciones para enviar mensajes de WhatsApp Business API utilizando fastapi y httpx.
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
    {"type": "reply", "reply": {"id": "sum", "title": "SUM"}},
    {"type": "reply", "reply": {"id": "residuos", "title": "Residuos"}},
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
                    message_body = message['text']['body']
                    
                    # Procesar cada mensaje individualmente
                    logger.info(f"  Mensaje recibido: - De (from_number): {from_number} - ID (message_id): {message_id} - Contenido (text:body): {message_body}")

                    # Responder al mensaje del remitente
                    wa_service = WhatsAppService()
                    response = await wa_service.send_text_message_to_user(from_number, "¡Gracias por tu mensaje!")
                    logger.info(f"Respuesta enviada: {response}")
            if 'statuses' in value:
                for status in value['statuses']:
                    message_id = status['id']
                    status = status['status']
                    logger.info(f"  Estado del mensaje id.{message_id}: {status}")
                                        
    return {
        "status": "success",
        "description": "Mensaje procesado exitosamente.",
    }



def enviar_respuesta(usuario_id: str, mensaje: str, botones: list[Dict]):
    """
    Envía un mensaje con botones al usuario.
    """
    respuesta = {
        "recipient_type": "individual",
        "to": usuario_id,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": mensaje},
            "action": {"buttons": botones}
        }
    }
    logger.info(f"Enviando respuesta: {json.dumps(respuesta, indent=2)}")


def manejar_mensaje(payload: Dict):
    """
    Maneja un mensaje entrante, responde automáticamente y registra la interacción.
    """
    entry = payload.get("entry", [])
    for item in entry:
        changes = item.get("changes", [])
        for change in changes:
            mensajes = change.get("value", {}).get("messages", [])
            for mensaje in mensajes:
                usuario_id = mensaje.get("from")
                texto = mensaje.get("text", {}).get("body")

                # Responder al mensaje inicial
                if texto:
                    logger.info(f"Mensaje recibido de {usuario_id}: {texto}")

                    # Enviar mensaje de bienvenida con menú
                    enviar_respuesta(
                        usuario_id,
                        "Hola! Gracias por tu mensaje. Bienvenido! A continuación te paso un menú de temas sobre el cual puedes hacerme las consultas que intentaré responder con mucho gusto.",
                        MENU_BUTTONS
                    )

                # Manejar selección del usuario (simulación de respuesta)
                if mensaje.get("type") == "interactive" and "button_reply" in mensaje:
                    seleccion = mensaje["button_reply"]["id"]
                    logger.info(f"El usuario {usuario_id} seleccionó la opción: {seleccion}")
