from .base_exceptions import ApplicationException

class FastAPIInitializationException(ApplicationException):
    """
    Excepción personalizada para errores en la inicialización de FastAPI.

    Args:
        detail (str): Detalle del error.
    """
    def __init__(self, detail: str, extra_data: dict = None):
        super().__init__(status_code=500, detail=detail, extra_data=extra_data)
