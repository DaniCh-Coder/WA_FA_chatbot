## exceptions/exceptions_handelrs_setup.py
## File containing the setup of the exception handlers for the FastAPI application
### There is no need of server_exceptions.py file in this case
from fastapi import FastAPI
from app.exceptions.server_exceptions_handler import (
    generic_exception_handler
)

def setup_generic_exceptions(app: FastAPI):
    exception_handlers = {
        generic_exception_handler: Exception
    }

    for exception, handler in exception_handlers.items():
        app.add_exception_handler(exception, handler)
