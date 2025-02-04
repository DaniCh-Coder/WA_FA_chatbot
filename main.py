'''
main: Se encarga de arrancar inicializar y comenzar la aplicación: 
    + Configurar el logger.
    + Registrar las rutas.
    + Generar una instancia de FastAPI y configurar el servidor y el tunel ngrok.
        + Iniciar el servidor uvicorn para FastAPI y el tunel ngrok para exponer el servidor local a internet.
Author: @DanielChristello - @Chreinvent - 2025
Version: 1.0
'''
from fastapi import FastAPI
from app.utils.ngrok_utils import start_ngrok
from app.utils.utils import configure_logging
from app.routes.webhook_routes import router as webhook_router
from app.config_setup.config_settings import get_settings


# Configuración del logger
logger = configure_logging(__name__)

# Carga de configuración
settings = get_settings()

# -------------------------------------------------------------------------------
# Crear la instancia de FastAPI
# --------------------------------------------------------------------------------
app = FastAPI(
    title="WhatsApp Chatbot API",
    description="API para manejar interacciones con WhatsApp y Meta",
    version="1.0.0",
)

# Registrar las rutas
app.include_router(webhook_router)

# Informar en el log
logger.info("Creación de instancias: [logger: OK, app: OK, rutas: OK, API Router: {webhook_router} - OK]")

#---------------------------------------------------------------------------------
# Función de arranque de la aplicación propiamente dicha
#---------------------------------------------------------------------------------
def start_application():
    """
    Inicia el túnel ngrok y el servidor Uvicorn para exponer la aplicación FastAPI.
    """
    try:
        logger.info("Iniciando el túnel ngrok...")
        start_ngrok()
    except Exception as e:
        logger.critical(f"Error crítico al iniciar ngrok: {e}")
        raise  # Mantén este error para detener el flujo de la aplicación si ngrok no arranca.


#---------------------------------------------------------------------------------
# main: Inicio de la aplicación
#---------------------------------------------------------------------------------
if __name__ == "__main__":
    
    # Iniciar la aplicación
    try:
        start_application()
    except Exception as e:
        logger.critical(f"No se pudo iniciar la aplicación: {e}")
        raise
    
    try:
        import uvicorn
        logger.info("Iniciando el servidor FastAPI con Uvicorn...")

        uvicorn.run("main:app", port=5000, log_level="info")
        logger.info("uvicorn.run se ha ejecutado y finalizado correctamente.")
    
    except Exception as e:
        logger.critical(f"Error crítico al iniciar el servidor FastAPI: {e}")
        raise