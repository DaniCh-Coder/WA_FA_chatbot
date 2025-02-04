# Estructura del Proyecto: WhatsApp Bot en Python

## Introducción
Este documento describe la estructura del proyecto **WA_FA_chatbot**, un bot de WhatsApp desarrollado en Python. Su propósito es facilitar la interacción entre un proveedor y un cliente mediante el envío y recepción de mensajes a través de WhatsApp.

La aplicación responde automáticamente a los mensajes de los usuarios, proporcionando un saludo y un menú con opciones predefinidas. Además, registra las selecciones de los usuarios en los logs del servidor.

## Organización del Proyecto
El proyecto está estructurado en directorios específicos para facilitar la modularidad y la escalabilidad. A continuación, se describe el propósito de cada uno de ellos.

### 1. `app/`
Contiene la lógica principal del bot y está organizada en submódulos:

- **`config_setup/`**: Maneja la configuración de la aplicación.
  - `config_settings.py`: Define la función `get_settings` para cargar la configuración.
  - `settings.py`: Define la clase `Settings`, que gestiona las variables de entorno.
  - `test_config_dependencies.py`: Contiene pruebas para verificar la carga de configuración.


- **`routes/`**: Define las rutas de la API.
  - `webhook_routes.py`: Implementa las rutas para manejar los webhooks de WhatsApp.

- **`schemas/`**: Define los esquemas de validación de datos.
  - `webhook_schema.py`: Define los esquemas de datos para los webhooks.

- **`services/`**: Implementa la lógica de negocio.
  - `wa_services.py`: Contiene las funciones para procesar mensajes de WhatsApp.
  - `README_wa_services.md`: Documentación de los servicios.

- **`utils/`**: Utilidades auxiliares.
  - `utils.py`: Funciones generales de la aplicación.
  - `ngrok_utils.py`: Funciones para gestionar túneles con Ngrok.

### 2. `docs/`
Contiene documentación relacionada con el proyecto.
- `images/`: Carpeta para almacenar imágenes de documentación.
- `Automatizacion-Whatssap.md`: Explica la automatización del bot.
- `README_Estructura.md`: Explica la estructura del proyecto.
- `README_env.md`: Explicación de las variables de entorno utilizadas.
- `README_settings.md`: Documentación sobre la configuración.
- `README_webhook_routes.md`: Documentación de las rutas webhook.
- `README_webhook.md`: Documentación sobre los esquemas webhook.

- `WA_Payload_Notification.md`: Explica los datos enviados por WhatsApp.
- `Markdown short guide.md`: Guía rápida sobre Markdown.

### 3. `tests/`
Contiene pruebas automatizadas del proyecto.
- `start/`: Contiene scripts de prueba iniciales para validar funcionalidades clave.
- `version_backup/`: Copias de seguridad de archivos clave del proyecto.

### 4. Archivos Raíz
- `.env`: Contiene las variables de entorno necesarias para la configuración del proyecto.
- `.gitignore`: Lista de archivos y carpetas que Git debe ignorar.
- `main.py`: Punto de entrada de la aplicación.
- `README.md`: Descripción general del proyecto.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.

## Conclusión
Esta estructura permite una organización clara y modular del código, facilitando su mantenimiento y escalabilidad. Cada carpeta tiene una función específica, lo que ayuda a mantener la separación de responsabilidades y a mejorar la mantenibilidad del código.

