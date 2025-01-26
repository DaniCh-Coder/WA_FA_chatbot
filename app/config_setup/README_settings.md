
# README: Configuración del archivo `settings.py`

## Introducción
El archivo `settings.py` es una parte fundamental de este proyecto, ya que centraliza la configuración de variables de entorno requeridas para la ejecución correcta de la aplicación. La utilización de `pydantic.BaseSettings` proporciona un manejo más robusto y profesional de estas variables, mejorando la validación, claridad y compatibilidad con FastAPI.

Este documento describe el contenido y la justificación de las decisiones de diseño adoptadas en el archivo `settings.py`.

---

## Justificación del diseño

### Uso de `pydantic.BaseSettings`
- **Validación integrada:** Asegura que todas las variables requeridas estén presentes y correctamente definidas.
- **Carga automática:** Permite cargar variables de un archivo `.env` o directamente de variables de entorno del sistema.
- **Compatibilidad con FastAPI:** Facilita la inyección de configuración como dependencia en los endpoints.

### Campo `Field`
Cada variable de entorno está documentada con el campo `Field`, que:
1. Proporciona una descripción clara del propósito de la variable.
2. Define si la variable es obligatoria o opcional.

### Configuración del archivo `.env`
El archivo `.env` permite manejar de forma segura las configuraciones sensibles, como tokens de acceso y URL, manteniéndolas fuera del código fuente.

### Validación inicial
Se valida que todas las variables requeridas estén configuradas correctamente al iniciar la aplicación, lo que previene errores durante su ejecución.

---

## Contenido del archivo `settings.py`

A continuación, se un contenido ejemplo ilustrativo de: `settings.py`:

```python
from pydantic import BaseSettings, Field, ValidationError

class Settings(BaseSettings):
    VERIFY_TOKEN: str = Field(..., description="Token para la verificación del webhook")
    ACCESS_TOKEN: str = Field(..., description="Token de acceso a la API de Meta")
    PHONE_NUMBER_ID: str = Field(..., description="ID del número de teléfono asociado a la cuenta de WhatsApp Business")
    META_API_VER: str = Field(..., description="Versión de la API de Meta utilizada")
    META_URL: str = Field(..., description="URL base de la API de Meta")
    RECIPIENT_ITEM_1: str = Field(None, description="ID del ítem del destinatario, si es requerido")
    RECIPIENT_WAID_1: str = Field(None, description="ID de WhatsApp del destinatario, si es requerido")

    class Config:
        env_file = ".env"  # Indica el archivo de variables de entorno
        env_file_encoding = "utf-8"  # Asegura la codificación correcta del archivo

# Probar la configuración al iniciar
try:
    settings = Settings()
except ValidationError as e:
    raise ValueError(f"Error al cargar las variables de entorno: {e}")

# Ejemplo de acceso
if __name__ == "__main__":
    print("Prueba inicial:")
    print(f"VERIFY_TOKEN: {settings.VERIFY_TOKEN}")
    print(f"ACCESS_TOKEN: {settings.ACCESS_TOKEN}")
    print(f"META_URL: {settings.META_URL}")
```

---

## Validación y manejo de errores
Si alguna de las variables obligatorias falta o tiene un valor inválido, se lanzará un error de validación al iniciar la aplicación. Esto asegura que los problemas de configuración se detecten de inmediato.

Ejemplo de error:
```plaintext
Error al cargar las variables de entorno: 1 validation error for Settings
ACCESS_TOKEN
  field required (type=value_error.missing)
```

---

## Prueba inicial
En el bloque `if __name__ == "__main__"`, se realiza una prueba básica para mostrar las variables cargadas desde el archivo `.env`. Esto es útil para verificar que las variables se están cargando correctamente y para depurar posibles problemas de configuración durante las etapas iniciales del desarrollo. El uso de este bloque permite inspeccionar rápidamente los valores actuales de las variables críticas sin necesidad de iniciar toda la aplicación.

---

## Uso en la aplicación
La configuración se utiliza principalmente para:
1. Verificar el token del webhook.
2. Acceder a la API de Meta con los tokens y URLs configurados.
3. Gestionar información del destinatario para enviar mensajes.

La instancia `settings` puede ser inyectada como dependencia en los controladores de FastAPI para simplificar el acceso a las variables de configuración.

