# Archivo de constantes de configuración de entorno

### Datos de configuración a continuación. https://developers.facebook.com/app (Panel de apps)
+ a. Datos del panel configuración de la API de Meta: 
  + a.1 ACCESS_TOKEN: token de identificación de Meta provisto por el panel de configuración de API de Whatssap (Panel de apps)
  + a.2 PHONE_NUMBER_ID: numero de identificación de whatsapp provisto por Meta + en el panel de configuración de API de Whatssap (Panel de apps)
  + a.3 APP_ID: numero de identificación de la app que estoy desarrollando provisto por Meta en el panel de configuración de API de Whatssap (Panel de apps)
  + a.4 RECIPIENT_WAID_#: numero de whatsapp de un contacto al que se le enviaran mensajes
  + a.5 RECIPIENT_ITEM_#: numero de identificación de un contacto al que se le enviaran mensajes

### b. Datos del panel de configuración Meta para cargar en el server (FastAPI):
+ b1. META_API_VER=v21.0  Lo informa meta en el panel de la app.
+ b2. META_URL=https://graph.facebook.com Es la url de la API de meta
  
### c. Datos propios del servidor de la app (FastAPI) en este caso para cargar en Meta
+ VERIFY_TOKEN=AppVerifyTokenABC123 Lo define el dueño del server y se carga en webhooks en Meta

### d. Datos de configuración de ngrok (pyngrok)
+ c.1 NGROK_AUTH_TOKEN: token de autenticación de ngrok
+ c.2 NGROK_COMMAND: linea de comando para iniciar ngrok
+ c.3 NGROK_TIMEOUT: tiempo de espera para que ngrok se inicie
