from fastapi import APIRouter, Request
from starlette.responses import PlainTextResponse
from app.schemas.webhook_schema import WebhookPayload, WebhookVerification
from app.config_setup.config_settings import get_settings
from app.services.wa_services import WhatsAppService, handle_webhook_POST_logic

import logging

# Configurar el logger
logger = logging.getLogger(__name__)

router = APIRouter()
whatsapp_service = WhatsAppService()
settings = get_settings()

@router.get("/", tags=["Home"])
def read_root():
    """Endpoint para comprobar que el servidor está activo."""
    return {
        "title": settings.APP_NAME,
        "version": "Beta",
        "message": "Server is running",
    }


# Validación del webhook: (Meta)
@router.get("/webhook", tags=["Webhook"])
async def verify_webhook(request: Request):
    """
    Verifica el webhook de WhatsApp.
    """
    logger.info("Verificando el webhook...")
    
    # Extraer parámetros de la solicitud
    params = dict(request.query_params)

    # Verificar si faltan parámetros requeridos
    required_params = {"hub.mode", "hub.verify_token", "hub.challenge"}
    missing_params = required_params - params.keys()

    if missing_params:
        logger.error(f"Parámetros faltantes: {missing_params}")
        # raise MissingParametersException(missing_params=list(missing_params))

    # Validar los parámetros usando el modelo Pydantic
    verification = WebhookVerification(**params)

    # Validar que el modo sea el esperado
    if verification.mode != "subscribe":
        logger.error(f"Modo no válido: {verification.mode}")
        # raise InvalidModeException(provided_mode=verification.mode, expected_mode="subscribe")

    # Validar el token
    if verification.verify_token == settings.VERIFY_TOKEN:
        logger.info("Webhook verificado exitosamente.")
        return PlainTextResponse(content=verification.challenge, status_code=200)

    # Lanzar excepción si el token no es válido
    # raise InvalidTokenException(provided_token=verification.verify_token, expected_token=settings.VERIFY_TOKEN)


@router.post("/webhook", tags=["Webhook"])
async def webhook_handler(payload: WebhookPayload):
    """
    Procesa los mensajes entrantes del webhook de WhatsApp.
    Solo delega el manejo de la lógica.
    """
    try:
        response = await handle_webhook_POST_logic(payload)
        return response
    except ValueError as e:
        # Manejo de errores específicos desde el servicio
        logger.error(f"Error en el webhook: {e}")
    except Exception as e:
        # Manejo general de errores no esperados
        logger.error(f"Error inesperado en el webhook: {e}")