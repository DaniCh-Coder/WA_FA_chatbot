'''
ngrok_utils.py
ngrok utilities: necessary functions to manage ngrok tunnels
Author: @DanielChristello - @Chreinvent - 2025
Version: 1.0
Este es un módulo de funciones para el manejo de túneles con ngrok
'''
import subprocess
import httpx
import time
from app.config_setup.config_settings import get_settings
from app.utils.utils import configure_logging


# Configuración del logger
logger = configure_logging(__name__)

# Configuraciones desde el archivo .env
settings = get_settings()
ngr_command = settings.NGROK_COMMAND
ngrok_timeout = settings.NGROK_TIMEOUT


def validate_ngrok_config():
    """
    Valida las configuraciones de ngrok.

    Raises:
        Ngrok Exception: Si las configuraciones de ngrok no son válidas.
    """
    if not ngr_command:
        logger.error("NGROK_COMMAND no puede estar vacío")
    if ngrok_timeout <= 0:
        logger.error("NGROK_TIMEOUT tiempo agotado. Debe ser mayor que cero.")

def get_ngrok_tunnel():
    """
    Consulta el estado actual de los túneles activos de ngrok.

    Returns:
        dict: Contiene la información del primer túnel activo si existe, o None si no hay túneles.

    Raises:
        NgrokException: Si ocurre un error al obtener el estado de ngrok.
    """
    logger.info(f"{__name__} Consultando la API de ngrok para obtener información de los túneles...")
    try:
        response = httpx.get("http://127.0.0.1:4040/api/tunnels")
        # Si la respuesta es exitosa, se registra el código de estado
        logger.info(f"{__name__} Respuesta de la API de ngrok: {response.status_code}")
        response.raise_for_status()  # Esto levantará una excepción si el código de estado es 4xx o 5xx
        data = response.json()
        if "tunnels" in data and len(data["tunnels"]) > 0:
            return data["tunnels"][0]  # Retorna los detalles del primer túnel
        return None  # Si no hay túneles, retorna None
    except httpx.RequestError as e:
        # Captura errores relacionados con la solicitud HTTP (por ejemplo, conexión fallida)
        logger.error(f"{__name__} Error al realizar la solicitud HTTP: {e}")
        return None  # No se puede conectar con la API de ngrok, retorna None
    except httpx.HTTPStatusError as e:
        # Captura errores relacionados con el estado de la respuesta (4xx, 5xx)
        logger.error(f"{__name__} Error al obtener datos de ngrok: {e}")
        return None  # El servidor respondió con un error, pero no se detiene el programa

def wait_for_ngrok(timeout=ngrok_timeout):
    """
    Espera a que ngrok inicie verificando periódicamente si hay un túnel activo.

    Args:
        timeout (int): Tiempo máximo de espera en segundos.

    Returns:
        dict: Información del túnel si se encuentra, None si no se encuentra dentro del tiempo límite.

    Raises:
        Exception: Si no se logra establecer un túnel en el tiempo límite.
    """
    for i in range(1, timeout + 1):
        logger.info(f"Esperando... {i}/{timeout} segundos")
        time.sleep(1)
        try:
            tunnel = get_ngrok_tunnel()
            if tunnel:
                return tunnel
        except Exception as e:
            logger.warning(f"Intento fallido al obtener túnel: {e}")
    raise ("Tiempo de espera agotado para establecer un túnel ngrok.")

def start_ngrok_tunnel():
    """
    Inicia un túnel de ngrok ejecutando el comando correspondiente en un terminal separado.

    Returns:
        bool: True si el comando se ejecuta correctamente.

    Raises:
        Ngrok Exception: Si ocurre un error al iniciar el túnel.
    """
    subprocess.run(["start", "cmd", "/k", ngr_command], shell=True, check=True)
    return True

def test_ngrok_tunnel():
    """
    Verifica si existe un túnel activo de ngrok y, si no lo encuentra, intenta crearlo.

    Returns:
        dict: Contiene el estado del túnel y su información (nombre, URL pública y URL privada) si está activo.
              En caso de error, incluye un mensaje descriptivo.
    """
    logger.info("Consultando túneles activos en ngrok...")
    
    tunnel = get_ngrok_tunnel()
    if tunnel:
        return {
            "status": "Túnel activo",
            "name": tunnel.get("name"),
            "public_url": tunnel.get("public_url"),
            "private_url": tunnel.get("config", {}).get("addr"),
        }

    logger.info("No se encontró un túnel activo. Intentando crearlo...")
    if start_ngrok_tunnel():
        logger.info("Esperando a que ngrok se inicie...")
        tunnel = wait_for_ngrok(timeout=10)
        if tunnel:
            return {
                "status": "Túnel creado con éxito",
                "name": tunnel.get("name"),
                "public_url": tunnel.get("public_url"),
                "private_url": tunnel.get("config", {}).get("addr"),
            }

    return {"status": "Error", "message": "No se pudo detectar ni crear el túnel ngrok"}

def start_ngrok():
    """
    Verifica y maneja el estado de un túnel ngrok y lo inicia si es necesario.

    Raises:
        NgrokException: Si ocurre algún problema al iniciar o verificar el túnel.
    """
    test_ngrok_tunnel()