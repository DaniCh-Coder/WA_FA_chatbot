# Notificaciones de Payload en WhatsApp Business API

Las notificaciones en WhatsApp Business API a través de Meta se envían como un payload JSON estructurado. Estas notificaciones se generan cuando ocurren eventos como la recepción de un mensaje, el cambio de estado de un mensaje, o el uso de una plantilla. A continuación, se explica su estructura y cómo procesarla.

---

## Ejemplo de Payload JSON para un Evento de Mensajes

Cuando suscribes el evento `messages` en los Webhooks de Meta, podrías recibir algo como esto:

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "1234567890",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15551234567",
              "phone_number_id": "1234567890"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Daniel"
                },
                "wa_id": "9876543210"
              }
            ],
            "messages": [
              {
                "from": "9876543210",
                "id": "ABGGFlA5ZmZmZDE6ABCDmZmZmZDEY", 
                "timestamp": "1672531200",
                "type": "text",
                "text": {
                  "body": "Hola, ¿cómo estás?"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

---

## Explicación de la Estructura

### 1. Nivel Raíz (`object` y `entry`)
- `object`: Indica el tipo de recurso afectado, en este caso, `whatsapp_business_account`.
- `entry`: Es una lista de eventos relacionados con tu cuenta. Cada elemento tiene un `id` (tu ID de cuenta) y los cambios reportados.

### 2. Dentro de `entry`
- `id`: Identificador único de tu cuenta de WhatsApp Business.
- `changes`: Lista que contiene los eventos notificados. 

### 3. Dentro de `changes`
- `field`: Define el tipo de evento. Aquí es `messages`, lo que indica que se trata de un mensaje recibido o enviado.
- `value`: Contiene los detalles del evento.

### 4. Dentro de `value`
- `messaging_product`: Especifica que se trata de WhatsApp.
- `metadata`: Detalles sobre el número de teléfono asociado:
  - `display_phone_number`: Número en formato legible.
  - `phone_number_id`: ID único del número en Meta.
- `contacts`: Información del contacto que envió el mensaje.
  - `profile.name`: Nombre del remitente, si está disponible.
  - `wa_id`: Identificador único de WhatsApp del contacto.
- `messages`: Lista de mensajes asociados al evento.

### 5. Dentro de `messages`
- `from`: Identificador único del usuario que envió el mensaje.
- `id`: ID único del mensaje.
- `timestamp`: Hora en que se envió el mensaje (en formato UNIX).
- `type`: Tipo de mensaje (`text`, `image`, `audio`, etc.).
- `text`: Contenido del mensaje. En el caso de tipo `text`, tiene un campo `body` con el texto.

---

## Ejemplo de Notificación de Estado de Mensaje

Si suscribes el evento `message_template_status_update`, recibirías algo como esto:

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "1234567890",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "statuses": [
              {
                "id": "ABGGFlA5ZmZmZDE6ABCDmZmZmZDEY",
                "recipient_id": "9876543210",
                "status": "delivered",
                "timestamp": "1672531210",
                "conversation": {
                  "id": "CONV1234",
                  "origin": {
                    "type": "business_initiated"
                  }
                }
              }
            ]
          },
          "field": "message_template_status_update"
        }
      ]
    }
  ]
}
```

### Detalles adicionales de este Payload:
- `statuses`: Lista que contiene estados de mensajes.
  - `id`: ID del mensaje cuyo estado ha cambiado.
  - `recipient_id`: El destinatario del mensaje.
  - `status`: Nuevo estado del mensaje (`sent`, `delivered`, `read`, etc.).
  - `conversation`: Información del contexto de la conversación.

---

## ¿Cómo procesarlo?

### 1. Parsear el JSON
Usa una librería como `json` en Python para convertir el payload en un diccionario:

```python
import json
payload = json.loads(raw_payload)
```

### 2. Acceder a datos específicos
Extrae los valores relevantes, como el tipo de mensaje y el contenido:

```python
entry = payload['entry'][0]
changes = entry['changes'][0]
value = changes['value']

message_type = value['messages'][0]['type']
message_body = value['messages'][0]['text']['body']
sender_id = value['messages'][0]['from']
```

### 3. Responde o registra el evento según sea necesario
Procesa los datos según tu lógica empresarial.

---


