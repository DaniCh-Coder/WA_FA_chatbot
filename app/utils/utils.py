
'''
utils.py
funciones de utilidad para la aplicación
utils functions to logging and other stuff
'''
import logging

# Función de configuración del logger
def configure_logging(name=None):
    if not logging.getLogger().hasHandlers():  # Evita reconfiguración
        log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"  # Definir formato correctamente

        logging.basicConfig(
            level=logging.INFO,
            format=log_format 
        )
    
    return logging.getLogger(name)

# Configuración del logger
logger = configure_logging(__name__)


def start_uvicorn():
    """
    Inicia el servidor UVICORN para FastAPI.

    Args:
        settings (Settings): Configuración de la aplicación.

    Raises:
        NgrokException: Si ocurre un error al iniciar el servidor.
    """
    import uvicorn
    logger.info("Iniciando el servidor FastAPI con Uvicorn...")
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=False, lifespan="on")
    logger.info("uvicorn.run se ha ejecutado y finalizado correctamente.")