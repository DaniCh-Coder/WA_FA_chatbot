## exeptions_setup.py
from fastapi import FastAPI

"""
    This script sets up the exceptions for the project.
"""

def exception_handlers_setup(app: FastAPI):
    """
    Inicializa todos los manejadores de excepciones personalizados en la aplicación.

    Args:
        app (FastAPI): Instancia de la aplicación FastAPI.
    """


    from app.exceptions.fastAPI_exceptions import FastAPIInitializationException
    from app.exceptions.fastAPI_exceptions_handler import fastapi_initialization_exception_handler
    from app.exceptions.server_exceptions_setup import setup_generic_exceptions
    from app.exceptions.ngrok_exceptions_setup import setup_ngrok_exceptions
    from app.exceptions.fastAPI_exceptions_setup import setup_fastAPI_exceptions
    # from app.exceptions.webhook_exeptions_setup import setup_webhook_exceptions

    # Inicialización de excepciones 
    
    # 1. Exceptiones qeu no requieren setups complejos (sin typos ni clases y por lo tanto sin setup específico.)
    app.add_exception_handler(FastAPIInitializationException, fastapi_initialization_exception_handler)
    
    # 2. Inicialización de excepciones específicas de ngrok
    setup_ngrok_exceptions(app)
    setup_fastAPI_exceptions(app)
    # setup_webhook_exceptions(app) 
        
    # Inicializa las excepciones genéricas de la aplicación. Son las que no tienen configuración específica.
    setup_generic_exceptions(app)
    
