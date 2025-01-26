## exceptions/ngrok_exceptions.py
from .base_exceptions import ApplicationException

class NgrokException(ApplicationException):
    """
    Excepción personalizada para errores relacionados con ngrok.

    Args:
        detail (str): Detalle del error.
    """
    def __init__(self, detail: str, extra_data: dict = None):
        super().__init__(status_code=500, detail=detail, extra_data=extra_data)
        
class NgrokStartException(NgrokException):
    """
    Excepción para errores específicos al manejar o iniciar el túnel ngrok.

    Args:
        detail (str): Detalle del error.
    """
    def __init__(self, detail: str, extra_data: dict = None):
        super().__init__(detail, extra_data=extra_data)