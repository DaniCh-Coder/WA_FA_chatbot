# Config Settings

'''Esta función crea y devuelve una instancia de la clase Settings.
    El propósito de usar una función en lugar de instanciar la clase directamente en el código principal es:
        Modularidad: Centraliza la creación de la configuración en un solo lugar.
        Reutilización: Puedes usar esta función en varias partes de tu código sin necesidad de repetir lógica o inicializar la configuración en múltiples lugares.
        Integración con FastAPI: Si estás utilizando FastAPI, puedes usar esta función como dependencia, lo que permite que el framework maneje su ciclo de vida.
'''
from app.config_setup.settings import Settings
from pydantic import ValidationError
from functools import lru_cache
from typing import Dict, Any
import logging

@lru_cache()
def get_settings() -> Settings:
    """Retorna una instancia cacheada de la configuración"""
    try:
        return Settings()
    except ValidationError as e:
        logging.error(f"Error al cargar la configuración: {str(e)}")
        raise

def initialize_logging(settings: Settings) -> None:
    """Inicializa la configuración de logging basada en los settings"""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def get_whatsapp_headers(settings: Settings) -> Dict[str, str]:
    """Retorna los headers necesarios para las peticiones a WhatsApp"""
    return {
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

def validate_webhook_token(token: str, settings: Settings) -> bool:
    """Valida el token del webhook"""
    return token == settings.VERIFY_TOKEN

def get_app_config(settings: Settings) -> Dict[str, Any]:
    """Retorna la configuración de la aplicación en formato JSON"""
    return {
        "app_name": settings.APP_NAME,
        "debug_mode": settings.DEBUG,
        "api_version": settings.META_API_VER,
        "docs_path": settings.DOCS_PATH
    }