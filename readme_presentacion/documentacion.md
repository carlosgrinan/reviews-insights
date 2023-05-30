# Documentación / memoria técnica descriptiva

## **Tecnologías que se han empleado**

- Para obtener retroalimentación de clientes, se utilizan varias [APIs de Google](https://developers.google.com/apis-explorer) mediante [Google API Python Client](https://github.com/googleapis/google-api-python-client):

  - APIs que necesitan autorización del usuario[^2]:
    - **[API de Gmail](https://developers.google.com/gmail/api/guides)**: para obtener emails de *Gmail* (por ejemplo, los recibidos por el departamento de atención al cliente).
    - **[APIs de Perfil de Empresa](https://developers.google.com/my-business/content/overview?hl=es)**: para obtener reseñas del negocio de *Google Maps* y *Búsqueda de Google*.
    - ~~**[APIs de Google Play Developer](https://developers.google.com/android-publisher?hl=es-419)**: para obtener reseñas de la app del negocio de  *Google Play Store*.~~
    - ~~**[Data API](https://developers.google.com/youtube/v3?hl=es-419)**: para obtener comentarios en videos de*Youtube* del negocio.~~
  - No necesitan autorización:
    - **[Places API](https://developers.google.com/maps/documentation/places/web-service/overview)**: para obtener reseñas del negocio de *Google Maps*[^1]. Nota: esta API no funciona con Google API Python Client y necesita su propio [cliente](https://github.com/googlemaps/google-maps-services-python).
- Para obtener la autorización del usuario:

  1. [ Librería JavaScript de autorización de terceros de Google](https://developers.google.com/identity/oauth2/web/guides/load-3p-authorization-library) se utilizará para obtener el código de autorización.
  2. El código será intercambiado por un [token](https://developers.google.com/identity/protocols/oauth2/web-server#httprest_3). [^3]
  3. [google-auth](https://googleapis.dev/python/google-auth/latest/user-guide.html) will be used to create Credentials from the token. The Credentials will be used by the aforementioned Google API Client to access Google APIs.
- To obtain insights (summary and/or tips) on the information, the language model [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5) from [OpenAI API](https://platform.openai.com/docs/introduction/overview) will be used through the [OpenAI Python library](https://github.com/openai/openai-python).
- TODO: Odoo

  - The frontend will use [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/).

[^1]: *Places API* solo permite obtener hasta 5 reseñas de un negocio, mientras que las *APIs de Perfil de Empresa* no tienen esta limitación. No obstante, requieren (además de la autorización del usuario) [solicitar acceso](https://developers.google.com/my-business/content/prereqs?hl=es#request-access).
    
[^2]: Las APIs de Google que ofrecen recursos protegidos  requieren autorización del propietario de los mismos (el usuario) mediante el protocolo OAuth2.0, aunque solamente se acceda a recursos abiertos al público (como las reseñas de las *APIs de Perfil de Empresa*).
    
[^3]: Opino que [google-auth-oauthlib](https://google-auth-oauthlib.readthedocs.io/en/latest/) añade complejidad innecesaria por lo que he optado por utilizar la librería estándar [requests](https://requests.readthedocs.io/en/latest/).
