"""
Webhook Payload Models.
Este archivo define los esquemas de los datos que se reciben en el webhook de Facebook.
Estos esquemas son utilizados por FastAPI para validar los datos recibidos.
"""
from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    from_: str
    text: Optional[dict]

class Change(BaseModel):
    value: dict

class Entry(BaseModel):
    changes: List[Change]

class WebhookPayload(BaseModel):
    entry: List[Entry]
