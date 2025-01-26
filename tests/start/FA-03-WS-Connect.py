"""
FastAPI Webhook Example
Author: @DanielChristello - 2024
Version: 0.3

Este servicio FastAPI está diseñado para manejar solicitudes de verificación de un webhook de Meta 
(WhatsApp Business API). Meta realiza una solicitud GET al endpoint especificado para verificar 
la autenticidad del servidor. Si el token enviado coincide con el configurado, devuelve el 
desafío proporcionado por Meta.

Documentación Meta: 
https://developers.facebook.com/docs/whatsapp/api/webhooks/inbound#verify-webhook
"""

from fastapi import FastAPI, Request, HTTPException # FastAPI class to handle the API requests and exceptios
from fastapi.responses import PlainTextResponse     # PlainTextResponse class to handle the responses of the API
import os                                           # os module to handle the environment variables
import logging                                      # logging module to handle the logging of the application
from dotenv import load_dotenv                      # load_dotenv function to load the environment variables from the .env file

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

    if not all([VERIFY_TOKEN, ACCESS_TOKEN, PHONE_NUMBER_ID]):
        raise ValueError("Faltan variables de entorno necesarias.")
except ValueError as e:
    logger.error(str(e))
    raise

# Define la aplicación FastAPI
app = FastAPI()

app.title = "Primer FastAPI con Webhook"
app.version = "0.3"

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
        Esto se hace mediante un proceso de verificación del webhook. 
        Meta solicita el webhook y espera una respuesta con el token de verificación.
        El endpoint /webhook verifica si el token recibido coincide con el token configurado en las variables de entorno.
        Meta envía una solicitud GET al endpoint que especificaste para el webhook, incluyendo tres parámetros clave:
            hub.mode: Indica la operación que se está realizando (normalmente "subscribe" para la verificación inicial).
            hub.verify_token: Un token que Meta espera que coincida con el que está configurado en tu servidor.
            hub.challenge: Un valor aleatorio que debe devolverse a Meta si la verificación es exitosa.
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

# Ejecución local del servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
    
    # Test first locally with: http://localhost:5000/
