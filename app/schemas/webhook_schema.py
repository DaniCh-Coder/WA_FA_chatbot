"""
    This module defines the Pydantic models for the webhook payload.
    These models are used to validate and parse the incoming webhook data.
..........................................................................
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class MessageType(str, Enum):
    """Tipos de mensajes que podemos recibir"""
    TEXT = "text"
    INTERACTIVE = "interactive"
    BUTTON = "button"
    DOCUMENT = "document"
    IMAGE = "image"

class TextMessage(BaseModel):
    """Estructura para mensajes de texto"""
    body: str

class ButtonReply(BaseModel):
    """Estructura para respuestas de botones"""
    id: str
    title: str

class InteractiveMessage(BaseModel):
    """Estructura para mensajes interactivos"""
    type: str
    button_reply: Optional[ButtonReply] = Field(None, alias="button_reply")

class Message(BaseModel):
    """Estructura principal del mensaje"""
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: MessageType
    text: Optional[TextMessage] = None
    interactive: Optional[InteractiveMessage] = None

    class Config:
        populate_by_name = True

class Metadata(BaseModel):
    """Metadata del mensaje"""
    display_phone_number: str
    phone_number_id: str

class Value(BaseModel):
    """Valor del cambio en el webhook"""
    messaging_product: str
    metadata: Metadata
    contacts: Optional[List[Dict[str, Any]]] = None
    messages: Optional[List[Message]] = None

class Change(BaseModel):
    """Estructura de cambios"""
    value: Value
    field: str

class Entry(BaseModel):
    """Entrada del webhook"""
    id: str
    changes: List[Change]

class WebhookPayload(BaseModel):
    """Payload completo del webhook"""
    object: str
    entry: List[Entry]

    def validate_payload(self) -> Optional[str]:
        """
        Valida la estructura del payload.
        Retorna un mensaje de error si hay problemas, o None si es válido.
        """
        if not self.entry:
            return "El payload está vacío."
        if not self.entry[0].changes:
            return "La estructura del payload es inválida."
        if not self.entry[0].changes[0].value.messages:
            return "No hay mensajes en el payload."
        return None
   
    def get_first_message(self) -> Optional[Message]:
        """Helper method para obtener el primer mensaje del payload"""
        if self.is_message_event():
            return self.entry[0].changes[0].value.messages[0]
        return None

    def is_message_event(self) -> bool:
        """Verifica si es un evento de mensaje"""
        return bool(self.entry and 
                   self.entry[0].changes and 
                   self.entry[0].changes[0].value.messages)

    def get_message_type(self) -> Optional[MessageType]:
        """
        Retorna el tipo del mensaje si el payload es válido.
        """
        message = self.get_first_message()
        if not message:
            return None
        return message.type
    
    def get_sender_phone_number(self) -> Optional[str]:
        """
        Obtiene el número de teléfono del remitente del primer mensaje.

        Returns:
            Optional[str]: Número del remitente o None si no hay mensajes.
        """
        if self.is_message_event():
            first_message = self.get_first_message()
            if first_message:
                return first_message.from_
        return None
    
class WebhookVerification(BaseModel):
    """Modelo para la verificación del webhook"""
    mode: str = Field(..., alias="hub.mode")
    verify_token: str = Field(..., alias="hub.verify_token")
    challenge: str = Field(..., alias="hub.challenge")

    class Config:
        population_by_name = True