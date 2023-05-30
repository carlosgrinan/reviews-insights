# Documentación / memoria técnica descriptiva

## **Tecnologías que se han empleado**

### Retroalimentación de clientes

Se utilizan varias [APIs de Google](https://developers.google.com/apis-explorer) mediante el [Cliente Python de las APIs de Google ](https://github.com/googleapis/google-api-python-client):

- APIs que necesitan autorización del usuario[^2]:
  - **[API de Gmail](https://developers.google.com/gmail/api/guides)**: para obtener emails de *Gmail* (por ejemplo, los recibidos por el departamento de atención al cliente).
  - **[APIs de Perfil de Empresa](https://developers.google.com/my-business/content/overview?hl=es)**: para obtener reseñas del negocio de *Google Maps* y *Búsqueda de Google*.
  - ~~**[APIs de Google Play Developer](https://developers.google.com/android-publisher?hl=es-419)**: para obtener reseñas de la app del negocio de  *Google Play Store*.~~
  - ~~**[Data API](https://developers.google.com/youtube/v3?hl=es-419)**: para obtener comentarios en videos de*Youtube* del negocio.~~
- No necesitan autorización:
  - **[Places API](https://developers.google.com/maps/documentation/places/web-service/overview)**: para obtener reseñas del negocio de *Google Maps*[^1]. Nota: esta API no funciona con el *Cliente Python de las APIs de Google*  y necesita su propio [cliente](https://github.com/googlemaps/google-maps-services-python).

Para obtener la autorización del usuario:

1. [ Librería JavaScript de autorización de terceros de Google](https://developers.google.com/identity/oauth2/web/guides/load-3p-authorization-library) se utiliza para obtener el código de autorización.
2. El código se intercambia por un [token](https://developers.google.com/identity/protocols/oauth2/web-server#httprest_3). [^3]
3. [google-auth](https://googleapis.dev/python/google-auth/latest/user-guide.html) crea *Credenciales*[^4] a partir del token. Las *Credenciales* son utilizadas por el *Cliente Python de las APIs de Google* para acceder a las APIs de Google.

### Resúmenes de la retroalimentación

Se utiliza el modelo de lenguaje [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5)[^5] de la [API de OpenAI](https://platform.openai.com/docs/introduction/overview) mediante la [Libreria Python de OpenAI](https://github.com/openai/openai-python).

### Integración en Odoo

He seguido la arquitectura estándar recomendada en Odoo 16:

- Frontend:
  - [Framework OWL](https://www.odoo.com/documentation/16.0/es/developer/reference/frontend/owl_components.html?highlight=owl): similar a *React*, es un framework web en JavaScript basado en componentes reactivos.
  - [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/) para el diseño y estructura de la UI.
  - Backend:

    - Módulo Base
    - Módulo Web
  - Base de Datos:

    - [PostgreSQL](https://www.postgresql.org/)

La app tiene ciertas particularidades debido a su uso de [multiprocesamiento](multiprocesamiento.md):

- Proxy inverso:

  - [Nginx](https://nginx.org/)
- Backend:

  - Módulo [Job Queue](https://apps.odoo.com/apps/modules/16.0/queue_job/).

[^1]: *Places API* solo permite obtener hasta 5 reseñas de un negocio, mientras que las *APIs de Perfil de Empresa* no tienen esta limitación. No obstante, requieren (además de la autorización del usuario) [solicitar acceso](https://developers.google.com/my-business/content/prereqs?hl=es#request-access).
    
[^2]: Las APIs de Google que ofrecen recursos protegidos  requieren autorización del propietario de los mismos (el usuario) mediante el protocolo OAuth2.0, aunque solamente se acceda a recursos abiertos al público (como las reseñas de las *APIs de Perfil de Empresa*).
    
[^3]: Existe una librería específica para esto: [google-auth-oauthlib](https://google-auth-oauthlib.readthedocs.io/en/latest/). Pero creo que añade complejidad innecesaria por lo que he optado por utilizar la librería estándar HTTP [requests](https://requests.readthedocs.io/en/latest/).
    
[^4]: Las Credenciales encapsulan los token y otros datos necesarios. *google-auth* se encarga de solicitar automáticamente un nuevo token de acceso cuando caduca.
    
[^5]: La app no utiliza la capacidad de recordar mensajes que tiene este modelo optimizado para chat. Lo he escogido simplemente porque [su rendimiento es similar al de otros como davinci pero a un precio inferior](https://platform.openai.com/docs/guides/chat/chat-vs-completions).
