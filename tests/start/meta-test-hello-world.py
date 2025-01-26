import os
import requests
from dotenv import load_dotenv
"""
Este script envía un mensaje de WhatsApp utilizando la API de Meta (anteriormente Facebook).

1. Carga las variables de entorno desde un archivo .env.
2. Define las variables necesarias para la API de Meta, como la versión de la API, el ID del número de teléfono, el token de acceso y el número de teléfono del destinatario.
3. Incluye una función `force_load_env` que fuerza la recarga de las variables de entorno desde el archivo .env, eliminando primero las variables relacionadas con la API de Meta del entorno actual.
4. Define una función `send_whatsapp_message` que construye y envía una solicitud POST a la API de WhatsApp Business para enviar un mensaje de plantilla.
5. La función `main` llama a `send_whatsapp_message` y maneja la respuesta, imprimiendo un mensaje de éxito o error según corresponda.

Primero tenga funcionando el tunnel ngrok. Puede utilizar ntrok-01-tunnel-test.py para ello.
El script se ejecuta llamando a la función `main` si el archivo se ejecuta directamente.
"""

# Cargar variables de entorno desde el archivo .env
load_dotenv(override=True)

# Variables de la API de Meta extraídas del entorno
VERSION = os.getenv("META_API_VER")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_PHONE = os.getenv("RECIPIENT_ITEM_1")

def send_whatsapp_message():
    """
    Envía un mensaje de WhatsApp usando la API de Meta.
    """
    # URL de la API de WhatsApp Business
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    
    # Encabezados para la solicitud
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    # Datos del mensaje
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_PHONE,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    
    # Enviar la solicitud POST
    response = requests.post(url, headers=headers, json=data)
    
    # Manejar la respuesta
    if response.status_code == 200:
        print("Mensaje enviado exitosamente.")
    else:
        print(f"Error al enviar el mensaje: {response.status_code} - {response.text}")
    return response.status_code

# Ejecutar la función y manejar la respuesta
def main():
    response = send_whatsapp_message()
    
    print(f"El script {__file__} ha sido ejecutado. - Status: {response}")

if __name__ == "__main__":
    main()
