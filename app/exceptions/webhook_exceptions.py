## exceptions/webhook_exceptions.py
from .base_exceptions import ApplicationException

class WebhookException(ApplicationException):
    """
    Excepción base para errores relacionados con webhooks.
    """
    pass

class InvalidTokenException(WebhookException):
    """
    Excepción para solicitudes con un token de verificación incorrecto.

    Args:
        provided_token (str): El token enviado por el cliente.
        expected_token (str): El token esperado por el servidor.

    Example:
        raise InvalidTokenException(provided_token="abc123", expected_token="xyz789")
    """
    def __init__(self, provided_token: str, expected_token: str):
        detail = f"Token de verificación incorrecto. Proporcionado: {provided_token}, Esperado: {expected_token}."
        extra_data = {"provided_token": provided_token, "expected_token": expected_token}
        super().__init__(status_code=403, detail=detail, extra_data=extra_data)

class MissingParametersException(WebhookException):
    """
    Excepción para solicitudes con parámetros faltantes.
    """
    def __init__(self, missing_params: list):
        detail = f"Faltan parámetros requeridos: {', '.join(missing_params)}."
        extra_data = {"missing_params": missing_params}
        super().__init__(status_code=400, detail=detail, extra_data=extra_data)

class InvalidModeException(Exception):
    def __init__(self, provided_mode: str, expected_mode: str):
        self.provided_mode = provided_mode
        self.expected_mode = expected_mode
        super().__init__(f"Modo inválido: {provided_mode}. Se esperaba: {expected_mode}.")