# Estructura del Proyecto WA_FA_chatbot

Este documento describe la estructura del proyecto `WA_FA_chatbot`, detallando la funcionalidad de cada directorio y archivo.

## Estructura del Proyecto

```
WA_FA_chatbot/
┣ app/
┃ ┣ config_setup/
┃ ┃ ┣ config_settings.py
┃ ┃ ┣ README_settings.md
┃ ┃ ┣ settings.py
┃ ┃ ┣ test_config_dependencies.py
┃ ┃ ┗ __init__.py
┃ ┣ exceptions/
┃ ┃ ┣ base_exceptions.py
┃ ┃ ┣ exeptions_setup.py
┃ ┃ ┣ fastAPI_exceptions.py
┃ ┃ ┣ fastAPI_exceptions_handler.py
┃ ┃ ┣ fastAPI_exceptions_setup.py
┃ ┃ ┣ ngrok_exceptions.py
┃ ┃ ┣ ngrok_exceptions_handler.py
┃ ┃ ┣ ngrok_exceptions_setup.py
┃ ┃ ┣ server_exceptions_handler.py
┃ ┃ ┣ server_exceptions_setup.py
┃ ┃ ┣ webhook_exceptions.py
┃ ┃ ┣ webhook_exceptions_handler.py
┃ ┃ ┣ webhook_exeptions_setup.py
┃ ┃ ┗ __init__.py
┃ ┣ routes/
┃ ┃ ┣ README_webhook_routes.md
┃ ┃ ┣ webhook_routes.py
┃ ┃ ┗ __init__.py
┃ ┣ schemas/
┃ ┃ ┣ README_webhook.md
┃ ┃ ┗ webhook_schema.py
┃ ┣ services/
┃ ┃ ┣ README_wa_services.md
┃ ┃ ┣ wa_services.py
┃ ┃ ┗ __init__.py
┃ ┣ utils/
┃ ┃ ┣ fa_utils.py
┃ ┃ ┣ ngrok_utils.py
┃ ┃ ┗ __init__.py
┃ ┗ __init__.py
┣ docs/
┃ ┣ images/
┃ ┃ ┗ ecosistema_chatbot.png
┃ ┣ Automatizacion-Whatssap.md
┃ ┣ Markdown short guide.md
┃ ┗ WA_Payload_Notification.md
┣ tests/
┃ ┣ start/
┃ ┃ ┣ FA-00-start-&-docs.py
┃ ┃ ┣ FA-01-start-&-title.py
┃ ┃ ┣ FA-02-start-&-tags.py
┃ ┃ ┣ FA-03-WS-Connect.py
┃ ┃ ┣ FA-04-WS-send-receive.py
┃ ┃ ┣ fastapi_utils_00.py
┃ ┃ ┣ meta-test-hello-world.py
┃ ┃ ┣ ngrok-01-tunnel-test.py
┃ ┃ ┣ ngrok-start-tunnel.py
┃ ┃ ┗ ngrok_00-test_start.py
┃ ┗ version_backup/
┃   ┣ fastapi_utils.py
┃   ┣ main.py
┃   ┣ ngrok_utils.py
┃   ┗ webhook.py
┣ .env
┣ .gitignore
┣ main.py
┣ README.md
┣ README_env.md
┣ README_webhook_routes.md
┣ requirements.txt
┗ __init__.py
```

## Descripción de Directorios y Archivos

### `app/`
Contiene la lógica principal de la aplicación.

- **config_setup/**: Configuración de la aplicación.
  - `config_settings.py`: Funciones para obtener y validar la configuración.
  - `README_settings.md`: Documentación sobre la configuración.
  - `settings.py`: Definición de la clase `Settings` para la configuración.
  - `test_config_dependencies.py`: Pruebas para la configuración.
  - `__init__.py`: Inicialización del módulo.

- **exceptions/**: Manejo de excepciones personalizadas.
  - `base_exceptions.py`: Excepciones base del proyecto.
  - `exeptions_setup.py`: Configuración de manejadores de excepciones.
  - `fastAPI_exceptions.py`: Excepciones específicas de FastAPI.
  - `fastAPI_exceptions_handler.py`: Manejadores de excepciones de FastAPI.
  - `fastAPI_exceptions_setup.py`: Configuración de excepciones de FastAPI.
  - `ngrok_exceptions.py`: Excepciones específicas de ngrok.
  - `ngrok_exceptions_handler.py`: Manejadores de excepciones de ngrok.
  - `ngrok_exceptions_setup.py`: Configuración de excepciones de ngrok.
  - `server_exceptions_handler.py`: Manejadores de excepciones del servidor.
  - `server_exceptions_setup.py`: Configuración de excepciones del servidor.
  - `webhook_exceptions.py`: Excepciones específicas de webhook.
  - `webhook_exceptions_handler.py`: Manejadores de excepciones de webhook.
  - `webhook_exeptions_setup.py`: Configuración de excepciones de webhook.
  - `__init__.py`: Inicialización del módulo.

- **routes/**: Definición de rutas de la API.
  - `README_webhook_routes.md`: Documentación sobre las rutas de webhook.
  - `webhook_routes.py`: Definición de rutas para manejar webhooks.
  - `__init__.py`: Inicialización del módulo.

- **schemas/**: Definición de esquemas de datos.
  - `README_webhook.md`: Documentación sobre los esquemas de webhook.
  - `webhook_schema.py`: Esquemas de datos para webhooks.
  - `__init__.py`: Inicialización del módulo.

- **services/**: Lógica de negocio y servicios.
  - `README_wa_services.md`: Documentación sobre los servicios de WhatsApp.
  - `wa_services.py`: Servicios para interactuar con la API de WhatsApp.
  - `__init__.py`: Inicialización del módulo.

- **utils/**: Funciones utilitarias.
  - `fa_utils.py`: Utilidades para FastAPI.
  - `ngrok_utils.py`: Utilidades para manejar ngrok.
  - `__init__.py`: Inicialización del módulo.

- `__init__.py`: Inicialización del módulo principal.

### `docs/`
Documentación del proyecto.

- **images/**: Imágenes utilizadas en la documentación.
  - `ecosistema_chatbot.png`: Diagrama del ecosistema del chatbot.

- `Automatizacion-Whatssap.md`: Documento sobre la automatización con WhatsApp.
- `Markdown short guide.md`: Guía corta sobre Markdown.
- `WA_Payload_Notification.md`: Documento sobre las notificaciones de payload en WhatsApp.

### `tests/`
Pruebas del proyecto.

- **start/**: Scripts de inicio y pruebas.
  - `FA-00-start-&-docs.py`: Ejemplo básico de FastAPI.
  - `FA-01-start-&-title.py`: Ejemplo con título y versión.
  - `FA-02-start-&-tags.py`: Ejemplo con tags.
  - `FA-03-WS-Connect.py`: Ejemplo de conexión con WebSocket.
  - `FA-04-WS-send-receive.py`: Ejemplo de envío y recepción con WebSocket.
  - `fastapi_utils_00.py`: Utilidades básicas para FastAPI.
  - `meta-test-hello-world.py`: Prueba de envío de mensaje con Meta.
  - `ngrok-01-tunnel-test.py`: Prueba de túnel ngrok.
  - `ngrok-start-tunnel.py`: Script para iniciar túnel ngrok.
  - `ngrok_00-test_start.py`: Prueba de inicio de ngrok.

- **version_backup/**: Copias de seguridad de versiones anteriores.
  - `fastapi_utils.py`: Utilidades para FastAPI.
  - `main.py`: Archivo principal de la aplicación.
  - `ngrok_utils.py`: Utilidades para ngrok.
  - `webhook.py`: Esquemas de datos para webhooks.

### Archivos de Configuración y Documentación

- `.env`: Archivo de variables de entorno.
- `.gitignore`: Archivo para ignorar archivos y directorios en Git.
- `main.py`: Archivo principal para iniciar la aplicación.
- `README.md`: Documentación principal del proyecto.
- `README_env.md`: Documentación sobre las variables de entorno.
- `README_webhook_routes.md`: Documentación sobre las rutas de webhook.
- `requirements.txt`: Lista de dependencias del proyecto.
- `__init__.py`: Inicialización del módulo raíz.
