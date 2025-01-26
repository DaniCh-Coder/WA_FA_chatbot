## exceptions/webhook_exceptions_handler.py
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.webhook_exceptions import InvalidTokenException, MissingParametersException, WebhookException, InvalidModeException

logger = logging.getLogger(__name__)

async def invalid_token_exception_handler(request: Request, exc: InvalidTokenException):
    """
    Manejador de excepciones personalizado para InvalidTokenException.

    Args:
        request (Request): Objeto de solicitud de FastAPI.
        exc (InvalidTokenException): Instancia de la excepción.

    Returns:
        JSONResponse: Respuesta JSON con los detalles del error.
    """
    logger.error(f"Error de Token Inválido: {exc.detail} - Extra data: {exc.extra_data}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Invalid Token",
            "details": exc.detail,
            "extra_data": exc.extra_data,
        },
    )

async def missing_parameters_exception_handler(request: Request, exc: MissingParametersException):
    """
    Manejador de excepciones para parámetros faltantes.

    Args:
        request (Request): Objeto de solicitud de FastAPI.
        exc (MissingParametersException): Instancia de la excepción.

    Returns:
        JSONResponse: Respuesta JSON con los detalles del error.
    """
    logger.error(f"Error de parámetros faltantes: {exc.detail} - Extra data: {exc.extra_data}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Missing Parameters",
            "details": exc.detail,
            "extra_data": exc.extra_data,
        },
    )

async def invalid_mode_exception_handler(request: Request, exc: InvalidModeException):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid Mode",
            "details": f"Modo proporcionado '{exc.provided_mode}' no es válido. Se esperaba '{exc.expected_mode}'."
        }
    )

async def webhook_exception_handler(request: Request, exc: WebhookException):
    """
    Manejador genérico para excepciones de webhooks.

    Args:
        request (Request): Objeto de solicitud de FastAPI.
        exc (WebhookException): Instancia de la excepción.

    Returns:
        JSONResponse: Respuesta JSON con los detalles del error.
    """
    logger.error(f"Webhook error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Webhook Error",
            "details": exc.detail,
            "extra_data": exc.extra_data,
        },
    )

