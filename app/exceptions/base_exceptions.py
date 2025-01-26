## 1. exceptions/base_exceptions.py
"""
Excepciones base del proyecto.
"""
from fastapi import HTTPException

class ApplicationException(HTTPException):
    """
    Excepción base para errores específicos de la aplicación.
    """
    def __init__(self, status_code: int, detail: str, extra_data: dict = None):
        super().__init__(status_code=status_code, detail=detail)
        self.extra_data = extra_data or {}
