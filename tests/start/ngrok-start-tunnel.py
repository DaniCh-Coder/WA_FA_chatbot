'''
start_ngrok_tunnel.py
Este script testea un tunel ngrok. Si no esta funcionando intenta crearlo.
Una vez que esta funcionando informa los datos del tunel
'''
import logging
from ngrok_utils import test_ngrok_tunnel, get_ngrok_tunnel

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    """
    Punto de entrada principal del script.
    Verifica y maneja el estado de un túnel ngrok.
    """
    try:
        result = test_ngrok_tunnel()
        logging.info(result)

        tunnel = get_ngrok_tunnel()
        logging.info(tunnel)
    except Exception as e:
        logging.error(f"Error en ejecución principal: {e}")
