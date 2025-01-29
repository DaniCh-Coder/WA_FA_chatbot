# Bot de Whatssap en python
WhatsApp bot in pure python

Este proyecto tiene como objetivo enviar y recibir mensajes a traves de whatssap entre un proveedor y un cliente para responder saludarlo y responder consultas sobre temas determinados en base a la selección de un aopción en un menú.

## Ecosistema
Los componentes del ecosistema de la aplicación resultante de este proyecto son los siguientes:
1. ***Mensajería***: WhatssApp
2. ***Server***: 
    2.1. **Uvicorn**: Servidor de aplicaciones ASGI. Controla y gestiona las conexiones entrada y salida de la aplicación.
    2.2. **ngrok**: Herramienta que permite exponer un servidor local a internet.
3. ***APIs***:
    3.1. **Whatssap Business API**: API de whatssap para empresas que permite enviar y recibir mensajes a través de la plataforma de whatssap.
    3.2.**FastAPI**: Framework web de alto rendimiento para construir APIs con Python 3.6+ basado en estándares abiertos.
4. ***Backend***:
    4.1. **Python**: Lenguaje de programación interpretado cuya filosofía hace hincapié en la legibilidad de su código.
    4.2. **Pydantic**: Librería para la validación de datos en Python.
    4.3. **httpx**: Cliente HTTP para Python 3, que proporciona una interfaz de cliente HTTP similar a las bibliotecas estándar de Python.
5. ***Numeros de teléfono de whatssap***:
    5.1 **Proveedor**: Numero cedido para pruebas por meta de whatssap
    5.2 **Cliente**: Numero asignado por el desarrollador para prueba de la aplicación

## Arquitectura
La arquitectura de la aplicación se basa en el diagrama de componentes de la figura:
![Ecosistema](docs/images/ecosistema_chatbot.png)
Y en consecuencia lo que hay que hacer es:
1. Configurar todo el ecosistema
2. Desarrollar e implementar la aplicación de los componentes dentro del circulo rojo.

##### Prerequisitos
- Conocimientos básicos de:
  - APIs. Qué son, cómo funcionan y cómo interactuar con ellas.
  - Herramientas de desarrollo de Meta: Qué es. Documentación. Blogs. Foros. Ejemplos. Etc.
  - Python. Cómo instalar paquetes, cómo ejecutar un script, cómo crear un entorno virtual, etc.
  - HTTP. Qué es, cómo funciona y cómo interactuar con él.
  - ASGI. Qué es, cómo funciona.
  - FastAPI. Qué es, cómo funciona y porqué fastAPI.
  - Pydantic. Qué es, cómo funciona y cómo interactuar con él.


### Configuración del ecosistema
#### Configuración de la API de WhatsApp Business
##### Requisistos
- Una cuenta de desarrollador de Meta: Si no tienes una, puedes crear una cuenta de desarrollador de Meta [aquí](https://developers.facebook.com/).
- Una app de negocios creada dentro del adminitrador de aplicaciones de meta. (business app). Si no tienes una, debes crear una app primero. Las intrucciones para esto se encuentran [aquí.](https://developers.facebook.com/docs/whatsapp/getting-started/create-business-app).
- Un número de teléfono de WhatsApp para empresas. Si no tienes uno, puedes solicitar uno [aquí.](https://developers.facebook.com/docs/whatsapp/getting-started/request-phone-number). Sin no quieres solicitarlo, meta te proporcionará uno para pruebas.
- Un número de teléfono de WhatsApp para pruebas. Si no tienes uno, puedes usar el tuyo propio. Pero este punto es mandatorio, necesitas uno o mas telefonos pra testear la aplicación como si fueran clientes/usuarios. Necesitas al menos un teléfono con WhatsApp para enviar y recibir mensajes, como lo haría un usuario/cliente normal.
##### Configurando la API de WhatsApp Business
Aquí, hay que configurar la API de WhatsApp Business. Para configurar la API de WhatsApp Business, sigue los pasos que se indican en la [documentación oficial](https://developers.facebook.com/docs/whatsapp/getting-started/).
Siguiendo los pasos de la documentación oficial, asegura de tener los siguientes puntos, cumplidos para disponeer de una versión gratuita de prueba de aplicaciones.
1. Crear una cuenta de desarrollador de Meta.
2. Crear una app de negocios en el administrador de aplicaciones de Meta.
3. Solicitar un número de teléfono de WhatsApp para empresas. Meta te provee uno si lo necesitas. Sino puedes usar un telefono de una empresa. Lo importante es que aquí estamos hablando del telefono de la empresa que va a responder los mensajes.
4. Configurar tu número de teléfono de WhatsApp para pruebas. Puedes usar tu propio número de teléfono si lo deseas. Es posible habilitar hasta 5 numeros de telefonos para este propósito. Pero necesitas al menos un número de teléfono para enviar y recibir mensajes, como lo haría un usuario/cliente normal.
   
#### Configuración de servidor de la aplicación.
##### Requisitos
- Un servidor para alojar la aplicación. Puede ser un servidor local o un servidor en la nube. En este caso se usará un servidor local.
- Un servidor local de aplicaciones ASGI. En este caso se usará Uvicorn.
- Un túnel para exponer el servidor local a internet. En este caso se usará ngrok.
- Un cliente HTTP para Python 3. En este caso se usará httpx.
- Un framework web de alto rendimiento para construir APIs con Python 3.6+. En este caso se usará FastAPI.
  - Una librería para la validación de datos en Python. En este caso se usará Pydantic.
- Un entorno virtual de Python. En este caso se usará venv.
  - Un editor de código. En este caso se usará Visual Studio Code.
