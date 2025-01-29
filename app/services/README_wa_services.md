# Módulo wa_services.py

Este módulo se encarga de manejar la API de WhatsApp Business. Contiene la lógica para enviar mensajes de texto y botones interactivos a través de la API de WhatsApp Business. Además, contiene la lógica para procesar solicitudes POST de webhook de WhatsApp Business API.

## Contenido del Módulo

### Clases y Funciones

#### `WhatsAppService`

Esta clase encapsula la lógica para interactuar con la API de WhatsApp Business. Contiene métodos para enviar mensajes de texto y botones interactivos.

- **Constructor (`__init__`)**: Inicializa la configuración y los encabezados necesarios para las solicitudes a la API de WhatsApp Business.
- **`re_format_number(from_number: str) -> str`**: Verifica si el número de teléfono del remitente es el número de teléfono de WhatsApp Business API y lo reformatea si es necesario.
- **`send_message(payload: Dict[str, Any]) -> Dict`**: Envía una solicitud POST a la API de WhatsApp Business con el payload proporcionado.
- **`send_text_message_to_user(phone_number: str, text: str) -> Dict`**: Envía un mensaje de texto simple al número de teléfono proporcionado.
- **`send_interactive_buttons(phone_number: str, body_text: str, buttons: list) -> Dict`**: Envía botones interactivos al número de teléfono proporcionado.

#### `handle_webhook_POST_logic(payload: WebhookPayload) -> dict`

Esta función maneja la lógica principal para procesar solicitudes POST de webhook. Itera sobre cada entrada en el payload, verifica si hay mensajes o estados, y procesa cada mensaje individualmente.

### Ejemplo de Uso

El módulo se utiliza principalmente para manejar mensajes entrantes de WhatsApp y responder con mensajes de texto o botones interactivos. Aquí hay un ejemplo de cómo se utiliza en el código:

```python
if 'messages' in value:
    for message in value['messages']:
        from_number = message['from']
        message_id = message['id']
        match message['type']:
            case 'text':
                message_body = message['text']['body']
                logger.info(f"Mensaje tipo texto recibido: - ID: {message_id}  - De (from_number): {from_number}  - Contenido (text:body): {message_body}")
                response1 = await wa_service.send_text_message_to_user(from_number, "Hola!")
                response2 = await wa_service.send_interactive_buttons(from_number, "Por favor, elije una opción:", MENU_BUTTONS)
                logger.info(f"Respuesta enviada: \n{response1}.\n{response2}")
            case 'interactive':
                interactive_type = message['interactive']['type']
                match interactive_type:
                    case 'button_reply':
                        button_id = message['interactive']['button_reply']['id']
                        button_title = message['interactive']['button_reply']['title']
                        logger.info(f"Botón interactivo presionado: {button_id, button_title}")
                    case 'list_reply':
                        button_id = message['interactive']['list_reply']['id']
                        button_title = message['interactive']['list_reply']['title']
                        logger.info(f"Botón interactivo presionado: {button_id, button_title}")
            case _:
                logger.info(f"Mensaje no procesado: {message}")
```

### Manejo de Estados

El módulo también verifica si hay estados en el payload y los procesa:

```python
if 'statuses' in value:
    for status in value['statuses']:
        message_id = status['id']
        status = status['status']
        logger.info(f"  Estado del mensaje id.{message_id}: {status}")
```

