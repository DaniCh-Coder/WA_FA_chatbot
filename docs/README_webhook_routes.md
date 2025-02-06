# Módulo de Rutas de Webhook

Este módulo define las rutas para manejar las interacciones de webhook con el servicio de WhatsApp usando FastAPI. Incluye endpoints para verificar y procesar solicitudes entrantes de webhook.

## Importaciones

```python
from fastapi import FastAPI, APIRouter, Request
from starlette.responses import PlainTextResponse
from app.schemas.webhook_schema import WebhookPayload, WebhookVerification
from app.config_setup.config_settings import get_settings
from app.services.wa_services import WhatsAppService, handle_webhook_POST_logic
import logging
```

- `FastAPI`, `APIRouter`, `Request`: Componentes de FastAPI para crear rutas y manejar solicitudes.
- `PlainTextResponse`: Usado para enviar respuestas en texto plano.
- `WebhookPayload`, `WebhookVerification`: Modelos Pydantic para validar datos de webhook.
- `get_settings`: Función para obtener la configuración de la aplicación.
- `WhatsAppService`, `handle_webhook_POST_logic`: Servicio y lógica para manejar interacciones de WhatsApp.
- `logging`: Módulo estándar de registro de Python.

## Configuración del Logger

```python
logger = logging.getLogger(__name__)
```

- Configura el logger para este módulo.

## Inicialización del Router y Servicio

```python
router = APIRouter()
whatsapp_service = WhatsAppService()
settings = get_settings()
```

- `router`: Inicializa el router de la API.
- `whatsapp_service`: Instancia del servicio de WhatsApp.
- `settings`: Obtiene la configuración de la aplicación.

## Endpoints

### Endpoint de Inicio

```python
@router.get("/", tags=["Home"])
def read_root():
    """Endpoint para comprobar que el servidor está activo."""
    return {
        "title": settings.APP_NAME,
        "version": "Beta",
        "message": "Server is running",
    }
```

- **Propósito**: Comprueba si el servidor está activo.
- **Devuelve**: Una respuesta JSON con el nombre de la aplicación, la versión y un mensaje indicando el estado del servidor.

### Endpoint de Verificación de Webhook
- **Propósito**: Verifica el webhook de WhatsApp.
- **Proceso**:
  - Registra el intento de verificación.
  - Extrae y verifica los parámetros requeridos de la solicitud.
  - Valida los parámetros usando modelos Pydantic.
  - Comprueba si el modo es "subscribe".
  - Valida el token de verificación.
- **Devuelve**: Una respuesta en texto plano con el desafío si la verificación es exitosa.

### Endpoint de Manejo de Webhook
- **Propósito**: Procesa los mensajes entrantes del webhook de WhatsApp.
- **Proceso**:
  - Delega la lógica de manejo a `handle_webhook_POST_logic`.
  - Registra errores específicos e inesperados.
- **Devuelve**: La respuesta de la lógica de manejo.
