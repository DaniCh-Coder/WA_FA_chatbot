'''
main: Se encarga de arrancar inicializar y comenzar la aplicación: 
    + Configurar el logger.
    + Registrar las rutas.
    + Configurar manejadores de excepciones.
    + Manejar errores críticos al arrancar la aplicación.
    + Generar una instancia de FastAPI y configurar el servidor y el tunel ngrok.
        + Iniciar el servidor uvicorn para FastAPI y el tunel ngrok para exponer el servidor local a internet.
'''
from fastapi import FastAPI
# from app.scripts.path_check import add_project_root_to_path
from app.utils.fa_utils import configure_logging
from app.utils.ngrok_utils import start_ngrok, start_uvicorn
from app.routes.webhook_routes import router as webhook_router
# from app.exceptions.exeptions_setup import exception_handlers_setup
from app.config_setup.config_settings import get_settings


"""
Inicializa los componentes globales de la aplicación.
"""

# Configuración del logger
logger = configure_logging(__name__)

# Carga de configuración
settings = get_settings()

# Crear la instancia de FastAPI
app = FastAPI(
    title="WhatsApp Chatbot API",
    description="API para manejar interacciones con WhatsApp y Meta",
    version="1.0.0",
)

# Configuración de manejadores de excepciones
#exception_handlers_setup(app)

# Registrar las rutas
app.include_router(webhook_router)

logger.info("Logger, app, setup_exception_handlers y rutas configurados correctamente.")
logger.info(f"Información del objeto APIRouter: {webhook_router}")
    
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




# Revisar path del proyecto antes de iniciar la aplicación si es necesario
# de lo contrario dejar add_project_root_to_path() comentado.
# add_project_root_to_path()


if __name__ == "__main__":
    
    # Iniciar la aplicación
    try:
        start_application()
    except Exception as e:
        logger.critical(f"No se pudo iniciar la aplicación: {e}")
        raise
    
    try:
        import uvicorn
        if not settings.UVICORN_APP:
            logger.critical("La configuración de UVICORN_APP no está definida.")
        logger.info("Iniciando el servidor FastAPI con Uvicorn...")
        uvicorn.run("main:app", port=5000, log_level="debug")
        logger.info("uvicorn.run se ha ejecutado y finalizado correctamente.")
    except Exception as e:
        logger.critical(f"Error crítico al iniciar el servidor FastAPI: {e}")
        raise