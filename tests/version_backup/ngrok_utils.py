'''
ngrok_utils.py
ngrrok utilities: necessary functions to manage ngrok tunnels
Author: @DanielChristello - 2024
Version: 1.0
Este es un módulo de funciones para el manejo de tuneles con ngrok
'''
import os
import logging
import subprocess
import httpx
import time
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Configuraciones desde el archivo .env
NGROK_COMMAND = os.getenv("NGROK_COMMAND", "").split()
NGROK_TIMEOUT = int(os.getenv("NGROK_TIMEOUT", 10))

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def exception_handler(func):
    """
    Decorador para manejar excepciones de forma centralizada y registrar errores en el log.
    
    Args:
        func (callable): Función a decorar.

    Returns:
        callable: Función decorada con manejo de excepciones.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error en {func.__name__}: {e}")
            return None
    return wrapper

@exception_handler
def validate_ngrok_config():
    """
    Valida las configuraciones de ngrok.
    """
    if not NGROK_COMMAND:
        raise ValueError("NGROK_COMMAND no puede estar vacío")
    if NGROK_TIMEOUT <= 0:
        raise ValueError("NGROK_TIMEOUT debe ser un valor positivo")

@exception_handler
def get_ngrok_tunnel():
    """
    Consulta el estado actual de los túneles activos de ngrok.

    Returns:
        dict: Contiene la información del primer túnel activo si existe, o None si no hay túneles.
    """
    try:
        response = httpx.get("http://127.0.0.1:4040/api/tunnels")
        response.raise_for_status()
        data = response.json()
        if "tunnels" in data and len(data["tunnels"]) > 0:
            return data["tunnels"][0]
        return None
    except httpx.RequestError as e:
        logging.error(f"Error al conectar con el endpoint de ngrok: {e}")
        return None

@exception_handler
def wait_for_ngrok(timeout=NGROK_TIMEOUT):
    """
    Espera a que ngrok inicie verificando periódicamente si hay un túnel activo.

    Args:
        timeout (int): Tiempo máximo de espera en segundos.

    Returns:
        dict: Información del túnel si se encuentra, None si no se encuentra dentro del tiempo límite.
    """
    for i in range(1, timeout + 1):
        logging.info(f"Esperando... {i}/{timeout} segundos")
        time.sleep(1)
        tunnel = get_ngrok_tunnel()
        if tunnel:
            return tunnel
    return None


    
@exception_handler
def start_ngrok_tunnel():
    """
    Inicia un túnel de ngrok ejecutando el comando correspondiente en un terminal separado.

    Returns:
        bool: True si el comando se ejecuta correctamente, False si ocurre algún error.
    """
    try:
        subprocess.run(["start", "cmd", "/k", "ngrok start metafastapi"], shell=True)
        return True
    except Exception as e:
        logging.error(f"Error al intentar iniciar el túnel ngrok: {e}")
        return False

@exception_handler
def test_ngrok_tunnel():
    """
    Verifica si existe un túnel activo de ngrok y, si no lo encuentra, intenta crearlo.

    Si el túnel no existe, ejecuta un comando para iniciar el túnel y vuelve a verificar.
    Finalmente, retorna el estado del túnel.

    Returns:
        dict: Contiene el estado del túnel y su información (nombre, URL pública y URL privada) si está activo.
              En caso de error, incluye un mensaje descriptivo.
    """
    logging.info("Consultando túneles activos en ngrok...")
    tunnel = get_ngrok_tunnel()
    if tunnel:
        return {
            "status": "Túnel activo",
            "name": tunnel.get("name"),
            "public_url": tunnel.get("public_url"),
            "private_url": tunnel.get("config", {}).get("addr"),
        }

    logging.info("No se encontró un túnel activo. Intentando crearlo...")
    if start_ngrok_tunnel():
        logging.info("Esperando a que ngrok se inicie...")
        tunnel = wait_for_ngrok(timeout=10)
        if tunnel:
            return {
                "status": "Túnel creado con éxito",
                "name": tunnel.get("name"),
                "public_url": tunnel.get("public_url"),
                "private_url": tunnel.get("config", {}).get("addr"),
            }

    return {"status": "Error", "message": "No se pudo detectar ni crear el túnel ngrok"}

#......................................................
# if __name__ == "__main__":
#    """
#   Punto de entrada principal del script.
#   Verifica y maneja el estado de un túnel ngrok.
#    """
#    result = test_ngrok_tunnel()
#    logging.info(result)
