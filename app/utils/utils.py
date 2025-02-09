
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