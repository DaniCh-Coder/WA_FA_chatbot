## exceptions/exceptions_handelrs_setup.py
## File containing the setup of the exception handlers for the FastAPI application
from fastapi import FastAPI
from app.exceptions.ngrok_exceptions_handler import (
    ngrok_exception_handler
)

from app.exceptions.ngrok_exceptions import (
    NgrokException
)


def setup_ngrok_exceptions(app: FastAPI):
    exception_handlers = {
        ngrok_exception_handler: NgrokException
    }

    for exception, handler in exception_handlers.items():
        app.add_exception_handler(exception, handler)
