## exceptions/exceptions_handelrs_setup.py
## File containing the setup of the exception handlers for the FastAPI application
from fastapi import FastAPI
from app.exceptions.fastAPI_exceptions_handler import (
    fastapi_initialization_exception_handler
)

from app.exceptions.fastAPI_exceptions import (
    FastAPIInitializationException
)


def setup_fastAPI_exceptions(app: FastAPI):
    exception_handlers = {
        fastapi_initialization_exception_handler: FastAPIInitializationException
    }

    for exception, handler in exception_handlers.items():
        app.add_exception_handler(exception, handler)
