
# Documentación del Archivo `schema/webhook.py`

Este documento describe el propósito, contenido y uso del archivo `schema/webhook.py` en un proyecto basado en FastAPI que interactúa con Webhooks de Meta.

---

## Introducción y Justificación

El archivo `schema/webhook.py` se encarga de definir las clases de datos necesarias para validar y estructurar las cargas útiles entrantes desde los webhooks de Meta. Estas clases, basadas en **Pydantic**, permiten garantizar que los datos recibidos tengan el formato correcto antes de ser procesados, lo que:
- Mejora la **seguridad** al evitar datos mal formados.
- Simplifica la **lógica del controlador** al delegar la validación de datos a un esquema claramente definido.
- Promueve una **separación de responsabilidades**, ya que la validación de datos se maneja por separado de la lógica de negocio.

### ¿Por Qué Usar Pydantic en FastAPI?
FastAPI utiliza Pydantic de manera nativa para la validación de datos. Definir clases en este archivo permite:
1. Validar automáticamente los datos de entrada según las especificaciones del webhook.
2. Generar documentación interactiva (Swagger UI) que detalla los esquemas esperados.
3. Minimizar errores y garantizar compatibilidad con el formato de los datos enviados por Meta.

---
## Criterios para la definición de clases
Las clases se definieron basándose en:

1. **Estructura del payload proporcionada por Meta:** La API de Meta describe cómo se estructura el JSON enviado a los webhooks, como este ejemplo simplificado:
```json
{
    "entry": [
        {
            "changes": [
                {
                    "value": {
                        "messages": [
                            {
                                "from": "123456789",
                                "text": {
                                    "body": "Hola, ¿cómo estás?"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```
De este ejemplo, se derivan las siguientes clases:

+ Message: Representa un mensaje individual dentro del campo messages.
+ Change: Representa un cambio dentro de la lista changes.
+ Entry: Representa cada entrada dentro del campo entry.
+ WebhookPayload: Es la raíz del esquema, representando todo el payload del webhook.

2. **Buenas prácticas de validación con FastAPI:** Utilizando Pydantic, se pueden definir modelos para validar y estructurar automáticamente los datos JSON. Esto asegura que los datos que llegan al controlador sean válidos y estén tipados correctamente.

3. **Separación lógica y claridad:** Cada clase representa un nivel lógico del payload, siguiendo la jerarquía de los datos JSON. Esto facilita su manipulación y comprensión.


## Contenido del Archivo `schema/webhook.py`

El archivo define las siguientes clases:

```python
from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    from_: str  # Número de origen del mensaje
    text: Optional[dict]  # Contenido textual del mensaje

class Change(BaseModel):
    value: dict  # Contiene datos relevantes del evento registrado

class Entry(BaseModel):
    changes: List[Change]  # Lista de cambios registrados para una entrada

class WebhookPayload(BaseModel):
    entry: List[Entry]  # Lista de entradas enviadas en la carga útil del webhook
```

### Explicación de las Clases
1. **`Message`**:
   - Representa un mensaje recibido.
   - Incluye:
     - `from_`: El número de origen que envió el mensaje.
     - `text`: Un diccionario opcional que puede contener información adicional sobre el mensaje.

2. **`Change`**:
   - Representa un cambio (evento) notificado por el webhook.
   - Contiene:
     - `value`: Un diccionario que incluye los datos del cambio.

3. **`Entry`**:
   - Representa una entrada en la carga útil del webhook.
   - Contiene:
     - `changes`: Una lista de cambios asociados con la entrada.

4. **`WebhookPayload`**:
   - Es la clase principal que valida toda la carga útil recibida.
   - Contiene:
     - `entry`: Una lista de entradas incluidas en la notificación.

---

## Uso de las Clases

### Implementación
FastAPI utiliza estas clases de manera implícita en los controladores para validar los datos entrantes. Por ejemplo:

```python
from fastapi import FastAPI, HTTPException
from schema.webhook import WebhookPayload

app = FastAPI()

@app.post("/webhook/")
async def handle_webhook(payload: WebhookPayload):
    # Procesar los datos validados
    for entry in payload.entry:
        for change in entry.changes:
            process_change(change.value)
    return {"status": "processed"}
```

### Flujo de Validación
1. Cuando un webhook de Meta envía datos al endpoint `/webhook/`, FastAPI:
   - Valida la carga útil entrante contra el esquema `WebhookPayload`.
   - Rechaza automáticamente las solicitudes con datos mal formados, devolviendo un error HTTP 422.
2. Una vez validados, los datos están disponibles como una instancia de `WebhookPayload`, lista para su procesamiento.

#### Uso detallado de las clases en el ciclo del programa
##### Clase WebhookPayload:
Representa el esquema general del payload entrante.
Es la entrada principal del endpoint /webhook.
##### Clase Entry:
Representa cada entrada dentro de la lista entry del webhook.
Usada en el bucle:

```pythonpython
for entry in payload.entry:
    # Procesa cada entrada
```
##### Clase Change:
Representa los cambios dentro de cada Entry.
Usada en el bucle:

```python
for change in entry.changes:
    # Procesa los cambios
```
##### Clase Message:

Define la estructura de un mensaje recibido, con el número del remitente y el texto. Aunque no se usa directamente en el controlador, se pueden mapear los datos si se desea ser más estricto:
```python
messages = [Message(**msg) for msg in change.value.get("messages", [])]
for message in messages:
    print(f"Mensaje de {message.from_}: {message.text['body']}")
```
##### Conclusión
Dónde usarlo: schemas/webhook.py se usa principalmente en el endpoint /webhook para validar y estructurar los datos entrantes.
+ Por qué incluirlo: Aumenta la claridad, facilita la validación y promueve la reutilización.
+ Cómo usarlo: Se utiliza directamente al definir el parámetro del endpoint, y sus clases internas permiten estructurar los datos a lo largo del procesamiento.
---

## Criterios y Bases para el Código

### Fuente de Información
Las clases se basan en la estructura esperada de las cargas útiles definidas en la [documentación oficial de Webhooks de Meta](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/components). Esto asegura:
- Compatibilidad total con el formato de los datos enviados.
- Flexibilidad para adaptarse a cambios futuros mediante modificaciones en el esquema.

### Principios Aplicados
1. **Separación de Responsabilidades**:
   - El archivo `schema/webhook.py` se enfoca únicamente en la validación de datos.
   - La lógica de negocio se maneja en los servicios y controladores.

2. **Escalabilidad**:
   - Las clases están diseñadas para ser fácilmente extensibles si Meta introduce nuevos campos o formatos.

3. **Simplicidad y Claridad**:
   - Cada clase refleja directamente un nivel en la jerarquía de datos del webhook.
   - Los nombres de las clases y atributos son descriptivos y alineados con la documentación de Meta.

---

## Beneficios del Enfoque
- **Reducción de Errores**: Las validaciones automáticas minimizan errores manuales en el procesamiento de datos.
- **Mantenimiento Simplificado**: La separación entre validación y lógica facilita la actualización del código.
- **Generación Automática de Documentación**: FastAPI genera documentación Swagger que detalla los esquemas, facilitando la colaboración.

---

## Conclusión

El archivo `schema/webhook.py` es esencial para garantizar la robustez y escalabilidad del manejo de webhooks de Meta en proyectos FastAPI. Su diseño refleja las mejores prácticas en validación y separación de responsabilidades, asegurando compatibilidad con las especificaciones de Meta y manteniendo el código mantenible y claro.