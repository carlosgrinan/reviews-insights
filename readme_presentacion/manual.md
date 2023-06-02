# **Manual de usuario**

## Instalación

1. Clona el [repositorio](https://github.com/carlosgrinan/reviews_insights) de la app dentro del directorio `Addons` de tu instalación de Odoo 16.
2. Instala o añade al fichero `requirements.txt` de tu instalación de Odoo 16 las dependencias especificadas como `external dependencies` en el fichero `__manifest__.py` de esta app: *requests*, *google-api-python-client*...
3. Instala las dependencias especificadas como `depends` (módulos de Odoo) en el fichero `__manifest__.py` de esta app.
4. Añade en el directorio de esta app un fichero `.env` con la siguiente información:

   ```
   OPENAI_API_KEY=your_openai_api_key

   GOOGLE_API_KEY=your_google_api_key
   CLIENT_ID=your_google_client_id
   PROJECT_ID=your_google_project_id
   CLIENT_SECRET=your_google_client_secret
   ```

   Sustituye los placeholders con tus credenciales de desarrollador de [Google](https://developers.google.com/identity/oauth2/web/guides/get-google-api-clientid?hl=es-419) y [OpenAi](https://platform.openai.com/account/api-keys).
5. TODO nginx...


## Uso

TODO incluir el mismo gif de uso que en la intro de la documentación
