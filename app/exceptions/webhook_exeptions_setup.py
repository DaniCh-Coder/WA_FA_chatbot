## exceptions/exceptions_handelrs_setup.py
## File containing the setup of the exception handlers for the FastAPI application
from fastapi import FastAPI
from app.exceptions.webhook_exceptions_handler import (
    invalid_token_exception_handler,
    missing_parameters_exception_handler,
    webhook_exception_handler,
    invalid_mode_exception_handler
)

from app.exceptions.webhook_exceptions import (
    InvalidTokenException,
    MissingParametersException,
    WebhookException,
    InvalidModeException
)


def setup_webhook_exceptions(app: FastAPI):
    exception_handlers = {
        InvalidTokenException: invalid_token_exception_handler,
        MissingParametersException: missing_parameters_exception_handler,
        WebhookException: webhook_exception_handler,
        InvalidModeException: invalid_mode_exception_handler
    }

    for exception, handler in exception_handlers.items():
        app.add_exception_handler(exception, handler)
