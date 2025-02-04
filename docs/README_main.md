# Documentación de main.py

## Descripción
El archivo `main.py` es el punto de entrada de la aplicación FastAPI para el chatbot de WhatsApp. 
Su función principal es inicializar la aplicación, configurar los componentes esenciales y ejecutar el servidor FastAPI con Uvicorn, 
Además de establece un túnel con ngrok para exponer la API en internet.

---

## Funcionalidades Principales
1. **Configurar el logger**: Permite registrar eventos y errores en la aplicación.
2. **Cargar configuración**: Obtiene los ajustes de la aplicación desde `config_settings.py`.
3. **Inicializar FastAPI**: Crea una instancia de la API con título, descripción y versión.
4. **Registrar las rutas**: Añade el `router` de `webhook_routes.py` a la aplicación.
5. **Iniciar túnel ngrok**: Permite exponer el servidor local a internet.
6. **Ejecutar el servidor FastAPI con Uvicorn**: Lanza el servidor en el puerto 5000.

---

## Estructura del Código

### 1. **Configuración Inicial**
- Se importa FastAPI y módulos de utilidades.
- Se configura el logger usando `configure_logging(__name__)`.
- Se carga la configuración con `get_settings()`.
- Se crea la instancia de FastAPI.
- Se agregan las rutas de `webhook_routes.py`.

### 2. **Función `start_application()`**
Esta función se encarga de:
- Iniciar el túnel ngrok mediante `start_ngrok()`.
- Manejar posibles errores críticos que puedan impedir el arranque de la aplicación.

### 3. **Inicio de la Aplicación**
Si el script se ejecuta como `__main__`:
- Se intenta arrancar la aplicación llamando a `start_application()`.
- Luego, se inicia el servidor Uvicorn en el puerto 5000.
- Se verifica si `UVICORN_APP` está definido en la configuración.

---

## Dependencias
Este script depende de los siguientes módulos:
- `FastAPI` para la creación de la API.
- `uvicorn` para correr el servidor.
- `app.utils.utils.configure_logging` para el manejo de logs.
- `app.utils.ngrok_utils.start_ngrok` para exponer el servidor con ngrok.
- `app.routes.webhook_routes` para gestionar las rutas del webhook.
- `app.config_setup.config_settings.get_settings` para la configuración.

---

## Cómo Ejecutar
1. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar el script:
   ```bash
   python main.py
   ```
   Esto iniciará ngrok y el servidor FastAPI en el puerto 5000.

---

## Manejo de Errores
- Si `ngrok` no arranca correctamente, se registra un error crítico y la aplicación se detiene.
- Si Uvicorn no puede iniciar, se muestra un error crítico en los logs y se interrumpe la ejecución.
- Se registran eventos importantes en los logs para facilitar el monitoreo y depuración.

---

## Notas Adicionales
- Se recomienda asegurarse de que `ngrok` esté correctamente instalado y configurado antes de ejecutar la aplicación.
- `UVICORN_APP` debe estar definido en la configuración para evitar fallos en el arranque de Uvicorn.
- Para exponer el servicio en producción, se deben considerar alternativas a `ngrok`, como un servidor con IP pública o un proxy inverso.

---

## Autor
Daniel E Christello - Chreinvet

