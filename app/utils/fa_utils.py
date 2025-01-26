"""
Funcionalidades de utilidad para el manejo de mensajes y errores en el webhook.
1. configure_logging: Configura el logger para registrar eventos importantes en formato JSON.
2. create_error_response: Crea respuestas de error en formato JSON, con soporte para logging.
3. validate_webhook_params: Valida parámetros clave del webhook con manejo de excepciones personalizadas.

Funciones de procesamiento por tipo de mensaje:
+ process_text_message: Para mensajes de texto.
+ process_image_message: Para mensajes de imagen.
+ process_button_message: Para mensajes de botones.
+ route_message: Enruta mensajes según su tipo y los procesa usando las funciones anteriores.
"""
import logging
import json
from fastapi.responses import JSONResponse
from app.schemas.webhook_schema import WebhookPayload, WebhookVerification

# Configuración de logging
def configure_logging(name=None):
    if not logging.getLogger().hasHandlers():  # Evita reconfiguración
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
    return logging.getLogger(name)

logger = configure_logging(__name__)

# Función para responder errores de forma consistente
def create_error_response(detail: str, status_code: int = 400):
    """
    Crea una respuesta de error consistente en formato JSON.

    Args:
        detail (str): Mensaje de error a incluir en la respuesta.
        status_code (int): Código de estado HTTP. Por defecto es 400.

    Returns:
        JSONResponse: Respuesta HTTP con el mensaje de error.
    """
    logger.error(json.dumps({"error": detail, "status_code": status_code}))
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail},
    )

# Validación de parámetros de webhook
def validate_webhook_params(mode: str, token: str, challenge: str, verify_token: str):
    """
    Valida los parámetros del webhook.

    Args:
        mode (str): Modo proporcionado en la solicitud (debería ser "subscribe").
        token (str): Token proporcionado para verificar la solicitud.
        challenge (str): Valor del desafío a devolver si la verificación es exitosa.
        verify_token (str): Token esperado para validación.

    Raises:
        MissingParametersException: Si faltan parámetros.
        InvalidModeException: Si el modo es incorrecto.
        InvalidTokenException: Si el token es inválido.

    Returns:
        str: El desafío si la validación es exitosa.
    """
    if not all([mode, token, challenge]):
        raise MissingParametersException("Faltan parámetros requeridos para la verificación del webhook.")

    if mode != "subscribe":
        raise InvalidModeException(provided_mode=mode)

    if token != verify_token:
        raise InvalidTokenException(provided_token=token, expected_token=verify_token)

    return challenge

# Procesamiento de mensajes
def process_text_message(from_number: str, text_body: str):
    """
    Procesa un mensaje de texto recibido.

    Args:
        from_number (str): Número del remitente.
        text_body (str): Cuerpo del mensaje recibido.
    """
    logger.info(f"Procesando mensaje de texto de {from_number}: {text_body}")
    # Aquí se puede agregar lógica personalizada para el mensaje de texto
    # Por ejemplo, análisis del contenido o ejecución de acciones específicas.
    return f"Mensaje procesado correctamente: {text_body}"

def process_image_message(from_number: str, image_url: str):
    """
    Procesa un mensaje de imagen recibido.

    Args:
        from_number (str): Número del remitente.
        image_url (str): URL de la imagen recibida.
    """
    logger.info(f"Procesando mensaje de imagen de {from_number}: {image_url}")
    # Aquí se puede agregar lógica personalizada para el mensaje de imagen
    return f"Imagen procesada correctamente: {image_url}"

def process_button_message(from_number: str, button_payload: str):
    """
    Procesa un mensaje de botón recibido.

    Args:
        from_number (str): Número del remitente.
        button_payload (str): Datos asociados al botón pulsado.
    """
    logger.info(f"Procesando mensaje de botón de {from_number}: {button_payload}")
    # Aquí se puede agregar lógica personalizada para el botón
    return f"Botón procesado correctamente: {button_payload}"

# Enrutamiento de mensajes según tipo
def route_message(payload: WebhookPayload):
    """
    Ruta un mensaje entrante según su tipo.

    Args:
        message (dict): Mensaje recibido en formato de diccionario.
    """
    from_number = message.get("from")
    message_type = message.get("type")

    if message_type == "text":
        text_body = message.get("text", {}).get("body", "")
        return process_text_message(from_number, text_body)

    elif message_type == "image":
        image_url = message.get("image", {}).get("url", "")
        return process_image_message(from_number, image_url)

    elif message_type == "button":
        button_payload = message.get("button", {}).get("payload", "")
        return process_button_message(from_number, button_payload)

    else:
        logger.warning(f"Tipo de mensaje desconocido recibido: {message_type}")
        return "Tipo de mensaje desconocido o no soportado."
