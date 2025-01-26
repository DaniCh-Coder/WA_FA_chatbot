from config_settings import get_settings  # Importa el archivo config.py donde está la función get_settings
from settings import Settings  # Importa la clase Settings del archivo settings.py
'''
Contiene un conjunto de pruebas diseñadas para verificar que la función get_settings del archivo config_settings.py 
devuelve correctamente una instancia de la clase Settings. Esto asegura que las configuraciones de la aplicación se cargan y funcionan como se espera, 
incluyendo las variables definidas en los entornos configurados (por ejemplo, el archivo .env).
'''
def test_get_settings():
    # Llamamos a la función para obtener la instancia de Settings
    settings = get_settings()

    # Ahora verificamos que la instancia de settings es de tipo Settings 
    assert isinstance(settings, Settings), "La función get_settings no retornó una instancia de Settings"
    print("Prueba pasada: Se creó correctamente una instancia de Settings")

    # También podemos verificar algunas de las variables de entorno para asegurarnos que se cargaron correctamente
    assert settings.VERIFY_TOKEN is not None  # Esto se basa en que la variable VERIFY_TOKEN debe estar definida en el .env
    assert settings.ACCESS_TOKEN is not None  # Esto se basa en que la variable ACCESS_TOKEN debe estar definida en el .env
    assert settings.META_URL is not None  # Esto se basa en que la variable META_URL debe estar definida en el .env

    print("Todas las pruebas pasaron correctamente.")

# Ejecutar el test
if __name__ == "__main__":
    test_get_settings()