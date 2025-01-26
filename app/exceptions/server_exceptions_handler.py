## exceptions/server_exceptions_handler.py
## This file contains the exception handler for unhandled exceptions in the application.
import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

async def generic_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "details": "An unexpected error occurred.",
            "exception": str(exc),
            "hint": "Please contact the system administrator."
        },
    )
