'''
start_ngrok_tunnel.py
Este script:
1. Testea un tunel ngrok. 
2.Si no esta funcionando intenta crearlo.
3. Luego arranca el servidor FastAPI.
'''
import logging
from ngrok_utils import test_ngrok_tunnel, get_ngrok_tunnel
from fastapi_utils import start_fastapi  # Import the start_fastapi function

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def start_ng_fa():
    """
    Punto de entrada principal del script.
    Verifica y maneja el estado de un túnel ngrok.
    """
    try:
        result = test_ngrok_tunnel()
        logging.info(result)

        tunnel = get_ngrok_tunnel()
        logging.info(tunnel)
     
        start_fastapi()  
      
    except Exception as e:
        logging.error(f"Error inesperado en ejecución principal start_ng_fa: {e}")
 
if __name__ == "__main__":
    try:
        # Llama al bucle asincrónico de forma correcta
        start_ng_fa()
    except Exception as e:
        logging.error(f"Error crítico al arrancar la aplicación: {e}")