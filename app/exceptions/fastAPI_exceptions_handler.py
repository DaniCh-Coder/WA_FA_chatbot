import logging
from fastapi.responses import JSONResponse
from requests import Request
from app.exceptions.fastAPI_exceptions import FastAPIInitializationException

logger = logging.getLogger(__name__)

async def fastapi_initialization_exception_handler(request: Request, exc: FastAPIInitializationException):
    """
    Manejador de excepciones para errores de inicialización de FastAPI.
    """
    logger.error(f"FastAPI initialization error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "FastAPI Initialization Error",
            "details": exc.detail,
            "hint": exc.hint,
            "extra": exc.extra,
        },
    )