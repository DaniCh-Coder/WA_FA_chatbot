import os
import sys
import logging

def try_main_import_again():
    """
    Intenta importar los modulos de main otra vez.
    """
    try:
        from app.scripts.path_check import add_project_root_to_path
        from app.utils.fa_utils import configure_logging
        from app.routes.webhook_routes import router as webhook_router
        from app.services.exceptions_handler import setup_exception_handlers
    except ImportError:
        logging.error(f"Error al importar el módulo los módulos de main: {e}")
        raise

# Llama directamente a la función antes de las importaciones locales
def add_project_root_to_path():
    """
    Añade la raíz del proyecto a sys.path si no está ya incluido.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)
        logging.info(f"Ruta del proyecto añadida a sys.path: {sys.path} \n")
        # try_main_import_again()
    else:
        logging.info(f"Ruta del proyecto correcta en sys.path: {sys.path} \n")

