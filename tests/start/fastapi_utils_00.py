"""
FastAPI Webhook Module
Author: @DanielChristello - 2024
Version: 0.0
Este es un módulo que debe incluirse en main.py
Esta es la primera versión que funciona y la más silmple por eso es versión 0.0
Este servicio FastAPI está diseñado para manejar solicitudes de verificación de un webhook de Meta
1. Verificar la validez de las notificaciones entrantes.
2. Procesar los mensajes recibidos y extraer la información relevante.
3. Responder automáticamente a los mensajes entrantes.
+ Meta enviará notificaciones al webhook cuando recibas un mensaje en tu cuenta de WhatsApp Business.
+ Este endpoint recibirá los datos enviados por Meta, que incluyen información sobre los mensajes entrantes.
+ El servidor responderá automáticamente a los mensajes con un mensaje de bienvenida.
Documentación Meta: 
https://developers.facebook.com/docs/whatsapp/api/webhooks/inbound#verify-webhook
"""

from fastapi import FastAPI, Request, HTTPException # FastAPI class to handle the API requests and exceptios
from fastapi.responses import PlainTextResponse     # PlainTextResponse class to handle the responses of the API
import os                                           # os module to handle the environment variables
import logging                                      # logging module to handle the logging of the application
from dotenv import load_dotenv                      # load_dotenv function to load the environment variables from the .env file
import requests                                     # requests module to handle HTTP requests
import json                                         # json module to handle the JSON data

# Configuración de logging
# Configura logging para registrar eventos importantes, como verificaciones exitosas o fallidas.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()                                       # Load the environment variables from the .env file
try:
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
    META_API_VER= os.getenv("META_API_VER")
    META_URL= os.getenv("META_URL")

    if not all([VERIFY_TOKEN, ACCESS_TOKEN, PHONE_NUMBER_ID, META_API_VER, META_URL]):
        raise ValueError("Faltan variables de entorno necesarias.")
except ValueError as e:
    logger.error(str(e))
    raise

app = FastAPI()
# Define la aplicación FastAPI
app = FastAPI()
app.title = "ngrok FastAPI con Webhook"
app.version = "1.0"
    
@app.get("/", tags=["Home"])   # Tag and Decorator for the root path
def read_root():
    """
    Endpoint principal para comprobar que el servidor está activo.
    """    
    return {"title": app.title, "version": app.version, "message": "Server is running"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
        Validación del webhook: (Meta) necesita asegurarse de que este server es del propietario del servidor que manejará las notificaciones. 
        Más información en: https://developers.facebook.com/docs/whatsapp/api/webhooks/inbound#verify-webhook
    """
    mode = request.query_params.get("hub.mode")             # obtiene el valor del parámetro "hub.mode" de la solicitud enviado por meta
    token = request.query_params.get("hub.verify_token")    # obtiene el valor del parámetro "hub.verify_token" de la solicitud enviado por meta
    challenge = request.query_params.get("hub.challenge")   # obtiene el valor del parámetro "hub.challenge" de la solicitud enviado por meta

    if not all([mode, token, challenge]):
        logger.warning("Faltan parámetros en la solicitud GET.")
        raise HTTPException(status_code=400, detail="Parámetros insuficientes en la solicitud.")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("Webhook verificado con éxito.")
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        logger.warning("Intento de verificación fallido.")
        if token != VERIFY_TOKEN:
            logger.warning(f"Token de verificación incorrecto. Meta: {token}. Local: {VERIFY_TOKEN}")
        if mode != "subscribe":
            logger.warning(f"Modo de verificación incorrecto: {mode}")
        raise HTTPException(status_code=403, detail="Verificación fallida")
    
@app.post("/webhook")
async def handle_messages(request: Request):
    try:
        body = await request.json()
        logger.info(f"Datos recibidos: {json.dumps(body, indent=2)}")

        entry = body.get("entry", [])
        if entry and "changes" in entry[0]:
            changes = entry[0]["changes"][0]
            logger.info(f"Cambios procesados: {json.dumps(changes, indent=2)}")
            
            messages = changes.get("value", {}).get("messages", [])
            if messages:
                message = messages[0]
                from_number = message.get("from")
                message_body = message.get("text", {}).get("body")
                
                logger.info(f"Mensaje de {from_number}: {message_body}")
                if from_number and message_body:
                    response_message = "Hola, ¿en qué puedo servirte?"
                    send_message_via_whatsapp(from_number, response_message)

        return {"status": "processed"}
    except Exception as e:
        logger.error(f"Error al procesar el mensaje: {str(e)}")
        raise HTTPException(status_code=500, detail="Error procesando el mensaje")

def send_message_via_whatsapp(to: str, message_template_name: str, language: str = "es"):
    url = f"{META_URL}/{META_API_VER}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": message_template_name,
            "language": {
                "code": language
            }
        }
    }
    logger.info(f"Enviando POST a {url} con payload: {json.dumps(payload, indent=2)}")
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        logger.info(f"Mensaje enviado exitosamente a {to}: {message_template_name}")
    else:
        logger.error(f"Error al enviar el mensaje a :{to} {response.status_code} - {response.text}")

def start_fastapi():
    """
    Inicia el servidor FastAPI.
    """
    import uvicorn
    uvicorn.run("fastapi_utils:app", host="0.0.0.0", port=5000, log_level="info")

# Ejecución local del servidor
#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=5000)
#    
    # Test first locally with: http://localhost:5000/
