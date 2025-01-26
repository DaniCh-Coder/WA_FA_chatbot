# app/routes/webhook_routes.py
"""
    Módulo de rutas para el webhook de WhatsApp.
"""
from fastapi import FastAPI, APIRouter, Request, HTTPException, Depends
from starlette.responses import PlainTextResponse
from app.schemas.webhook_schema import WebhookPayload, WebhookVerification
from app.config_setup.config_settings import get_settings
from app.services.wa_services import WhatsAppService
from app.exceptions.webhook_exceptions import InvalidTokenException, MissingParametersException, InvalidModeException
from app.exceptions.webhook_exceptions_handler import invalid_token_exception_handler, missing_parameters_exception_handler, invalid_mode_exception_handler

# from app.services.llm import LLMService
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

router = APIRouter()
whatsapp_service = WhatsAppService()
# llm_service = LLMService()

settings = get_settings()

MENU_BUTTONS = [
    {"type": "reply", "reply": {"id": "pileta", "title": "Pileta"}},
    {"type": "reply", "reply": {"id": "tenis", "title": "Tenis"}},
    {"type": "reply", "reply": {"id": "sum", "title": "SUM"}},
    {"type": "reply", "reply": {"id": "residuos", "title": "Residuos"}}
]

# Endpoint principal para comprobar que el servidor está activo.
@router.get("/", tags=["Home"])   # Tag and Decorator for the root path
def read_root():
    """
    Define la respuesta al acceso a la raíz del servidor.
    Normalmente se usa ingresando la url base del servidor en un navegador.
    """    
    return {"title": settings.APP_NAME, "version": "Beta", "message": "Server is running"}

# Validación del webhook: (Meta)
@router.get("/webhook", tags=["Webhook"])
async def verify_webhook(request: Request):
    """
    Verifica el webhook de WhatsApp.
    """
    try:
        # Extraer parámetros de la solicitud
        params = dict(request.query_params)

        # Verificar si faltan parámetros requeridos
        required_params = {"hub.mode", "hub.verify_token", "hub.challenge"}
        missing_params = required_params - params.keys()

        if missing_params:
            raise MissingParametersException(missing_params=list(missing_params))

        # Validar los parámetros usando el modelo Pydantic
        verification = WebhookVerification(**params)

        # Validar que el modo sea el esperado
        if verification.mode != "subscribe":
            raise InvalidModeException(provided_mode=verification.mode, expected_mode="subscribe")

        # Validar el token
        if verification.verify_token == settings.VERIFY_TOKEN:
            logger.info("Webhook verificado exitosamente.")
            return PlainTextResponse(content=verification.challenge, status_code=200)

        # Lanzar excepción si el token no es válido
        raise InvalidTokenException(provided_token=verification.verify_token, expected_token=settings.VERIFY_TOKEN)

    except MissingParametersException as e:
        # Manejo de parámetros faltantes
        return await missing_parameters_exception_handler(request, e)

    except InvalidModeException as e:
        # Manejo de modo inválido
        return await invalid_mode_exception_handler(request, e)

    except InvalidTokenException as e:
        # Manejo de token inválido
        return await invalid_token_exception_handler(request, e)


@router.post("/webhook")
async def webhook_handler(payload: WebhookPayload):
    """
        Maneja los mensajes entrantes de WhatsApp
        Un usuario de WA envia un mensaje y se procesa en este endpoint.
    """
    try:
        if not payload.is_message_event():
            return {"status": "ok"}

        message = payload.get_first_message()
        if not message:
            return {"status": "ok"}

        # Enviar menú de botones si es mensaje de texto
        if message.type == "text":
            await whatsapp_service.send_interactive_buttons(
                message.from_,
                "Elige sobre qué tema quieres preguntarme:",
                MENU_BUTTONS
            )
        
        # Procesar selección de botón
        elif message.type == "interactive" and message.interactive:
            selected_topic = message.interactive.button_reply.id
            await whatsapp_service.send_text_message(
                message.from_,
                f"Por favor, escribe tu consulta sobre {selected_topic}"
            )

        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Webhook handler error: {str(e)}")
        return {"status": "error", "message": str(e)}
