"""
Este módulo contiene la configuración de la aplicación.
Construye una clase con todas las variables de entorno necesarias y valida su debida existencia.
"""
from pydantic_settings import BaseSettings   
from pydantic import Field, ValidationError
from typing import Optional

class Settings(BaseSettings):
    # WhatsApp/Meta Configuration
    VERIFY_TOKEN: str = Field(..., description="Token para la verificación del webhook")
    ACCESS_TOKEN: str = Field(..., description="Token de acceso a la API de Meta")
    PHONE_NUMBER_ID: str = Field(..., description="ID del número de teléfono asociado a la cuenta de WhatsApp Business")
    META_API_VER: str = Field(..., description="Versión de la API de Meta utilizada")
    META_URL: str = Field(..., description="URL base de la API de Meta")
    
    # Recipient Configuration
    RECIPIENT_ITEM_1: str = Field(None, description="ID del ítem del destinatario, si es requerido")
    RECIPIENT_WAID_1: str = Field(None, description="ID de WhatsApp del destinatario, si es requerido")
    
    # Application Configuration
    APP_ID: str = Field(..., description="ID de la aplicación")
    APP_NAME: str = Field(default="WhatsApp Q&A Bot", description="Nombre de la aplicación")
    
    # Ngrok Configuration    
    NGROK_AUTH_TOKEN: str = Field(..., description="Token de autenticación de ngrok")
    NGROK_COMMAND: str = Field(..., description="Comando para ngrok")
    NGROK_TIMEOUT: int = Field(..., description="Tiempo de espera para ngrok")
    
    # Debug Configuration
    DEBUG: bool = Field(None, description="Modo de depuración")
    
    # LLM Configuration
    HUGGINGFACE_TOKEN: Optional[str] = Field(None, description="Token de HuggingFace para acceso a modelos")
    MODEL_NAME: str = Field(default="google/flan-t5-small", description="Nombre del modelo a utilizar")

    # Path Configuration
    DOCS_PATH: str = Field(default="./docs", description="Ruta a los documentos de conocimiento")
    MODELS_PATH: str = Field(default="./models", description="Ruta a los modelos de lenguaje")
    
    class Config:
        model_config = {
        "env_file": ".env",  # Archivo de variables de entorno
        "env_file_encoding": "utf-8",  # Codificación del archivo
        "extra": "allow"  # Permite variables adicionales como PYTHONPATH
    }   


    @property
    def meta_api_url(self) -> str:
        """Construye la URL completa de la API de Meta"""
        return f"{self.META_URL}/{self.META_API_VER}"
    
    @property
    def whatsapp_api_url(self) -> str:
        """Construye la URL completa para la API de WhatsApp"""
        return f"{self.meta_api_url}/{self.PHONE_NUMBER_ID}/messages"

# Probar la configuración al iniciar
try:
    settings = Settings()
except ValidationError as e:
    raise ValueError(f"Error al cargar las variables de entorno: {e}")

# Ejemplo de acceso
if __name__ == "__main__":
    print(f"VERIFY_TOKEN: {settings.VERIFY_TOKEN}")
    print(f"ACCESS_TOKEN: {settings.ACCESS_TOKEN}")
    print(f"META_API_VER: {settings.META_API_VER}")
    print(f"META_URL: {settings.META_URL}")
    print(f"PHONE_NUMBER_ID: {settings.PHONE_NUMBER_ID}")
    print(f"RECIPIENT_ITEM_1: {settings.RECIPIENT_ITEM_1}")
    print(f"RECIPIENT_WAID_1: {settings.RECIPIENT_WAID_1}")
    print(f"APP_ID: {settings.APP_ID}")
    print(f"NGROK_AUTH_TOKEN: {settings.NGROK_AUTH_TOKEN}")
    print(f"NGROK_COMMAND: {settings.NGROK_COMMAND}")
    print(f"NGROK_TIMEOUT: {settings.NGROK_TIMEOUT}")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"HUGGINGFACE_TOKEN: {settings.HUGGINGFACE_TOKEN}")
    print(f"MODEL_NAME: {settings.MODEL_NAME}")
    print(f"DOCS_PATH: {settings.DOCS_PATH}")
    print(f"MODELS_PATH: {settings.MODELS_PATH}")
    print(f"meta_api_url: {settings.meta_api_url}")
    print(f"whatsapp_api_url: {settings.whatsapp_api_url}")
    print(f"APP_NAME: {settings.APP_NAME}")
    print(f"LLM Configuration: {settings.LLM_CONFIG}")
    print(f"Path Configuration: {settings.PATH_CONFIG}")
    print(f"Recipient Configuration: {settings.RECIPIENT_CONFIG}")
    print(f"WhatsApp/Meta Configuration: {settings.WHATSAPP_META_CONFIG}")
    print(f"Application Configuration: {settings.APP_CONFIG}")
    print(f"Ngrok Configuration: {settings.NGROK_CONFIG}")
    print(f"Debug Configuration: {settings.DEBUG_CONFIG}")
   
