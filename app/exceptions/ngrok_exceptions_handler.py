## exceptions/ngrok_exception_handler.py
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.ngrok_exceptions import NgrokException, NgrokStartException

logger = logging.getLogger(__name__)

async def ngrok_exception_handler(request: Request, exc: NgrokException):
    """
    Manejador de excepciones para errores relacionados con ngrok.

    Args:
        request (Request): Objeto de solicitud de FastAPI.
        exc (NgrokException): Instancia de la excepción.

    Returns:
        JSONResponse: Respuesta JSON con los detalles del error.
    """
    logger.error(f"Ngrok error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Ngrok Error",
            "details": exc.detail,
        },
    )

async def ngrok_start_exception_handler(request: Request, exc: NgrokStartException):
    """
    Manejador para errores relacionados específicamente con el inicio de túneles ngrok.
    """
    logger.critical(f"Error crítico en start_ngrok: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Ngrok Start Error",
            "details": exc.detail,
        },
    )