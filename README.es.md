# Integración de la API de OpenAI con varias API de Google para generar información sobre los comentarios de los clientes

El objetivo de este proyecto es desarrollar un[Odoo](https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started.html)aplicación que proporciona información breve basada en inteligencia artificial sobre los comentarios de los clientes.

## Motivación

Los costos asociados con las revisiones y clasificaciones humanas de datos basados ​​en texto a menudo conducen a su descuido en favor de datos numéricos, que pueden analizarse automáticamente en plataformas como Google Analytics. Los avances recientes y la mayor accesibilidad de los modelos AI Language Generative también han hecho posible automatizar el análisis de información basada en texto. Al combinar análisis de ambos tipos de datos, las empresas pueden obtener conocimientos más completos que incorporar en su toma de decisiones.
Para poner en marcha este proyecto, nos centraremos en analizar los comentarios de los clientes. Sin embargo, el mismo enfoque se puede aplicar a otros tipos de datos valiosos basados ​​en texto.

## Herramientas

-   Para obtener comentarios de los clientes, varios[API de Google](https://developers.google.com/apis-explorer)será utilizado a través[Cliente API de Google](https://github.com/googleapis/google-api-python-client):

    -   Necesita autorización de Oauth2.0:
        -   **[API de Gmail](https://developers.google.com/gmail/api/guides)**: para obtener correos electrónicos de atención al cliente de_Gmail_.
        -   TODO:**Business Profile APIs**: para obtener opiniones de los clientes de_mapas de Google_y_Búsqueda de Google_.
        -   TODO:**API para desarrolladores de Google Play**: para obtener reseñas de aplicaciones de_Tienda de juegos de Google_.
        -   TODO:**datos de la API**: para obtener comentarios sobre videos de_YouTube_.
    -   No necesita autorización (datos disponibles públicamente):
        -   **[API de lugares](https://developers.google.com/maps/documentation/places/web-service/overview)**: para obtener hasta 5 reseñas de un_mapas de Google_lugar. Tenga en cuenta que esta API no funciona con el cliente API de Google y necesita su propia[cliente](https://github.com/googlemaps/google-maps-services-python)
-   Para obtener el consentimiento del usuario para acceder a los recursos protegidos de las API de Google que requieren autorización Oauth2.0:

    1.  [Biblioteca de JavaScript de autorización de Google 3P](https://developers.google.com/identity/oauth2/web/guides/load-3p-authorization-library)se utilizará para obtener un código de autorización
    2.  El código de autorización será canjeado por un[simbólico](https://developers.google.com/identity/protocols/oauth2/web-server#httprest_3). He encontrado[google-auth-oauthlib](https://google-auth-oauthlib.readthedocs.io/en/latest/)para complicar demasiado la tarea, así que opté por una solicitud HTTP simple.
    3.  [google-autorización](https://googleapis.dev/python/google-auth/latest/user-guide.html)se utilizará para crear Credenciales a partir del token. Las Credenciales serán utilizadas por el Cliente API de Google antes mencionado para acceder a las API de Google.
-   Para obtener insights (resumen y/o tips) sobre la información, el modelo de lenguaje[gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5)de[API de IA abierta](https://platform.openai.com/docs/introduction/overview)se utilizará a través de la[Biblioteca Open AI Python](https://github.com/openai/openai-python).
-   TODO: Odoo

    -   La interfaz utilizará[Oreja](https://getbootstrap.com/docs/5.0/getting-started/introduction/).

## Hitos

### Obtención de comentarios de los clientes

-   [x] Configure una cuenta de desarrollador para acceder a las API de Google.
-   [x] Obtenga datos disponibles públicamente de una API de Google (reseñas de la API de Places).
-   [x] Obtenga recursos protegidos de una API de Google (correos electrónicos de la API de Gmail).

### Obtención de información

-   [x] Configure una cuenta de desarrollador para acceder a la API de OpenAI.
-   [x] Refinando el aviso. Este paso tuvo lugar el[parque infantil openai](https://platform.openai.com/playground)para concentrarse en la indicación y la respuesta.
-   [x] Obtenga información a través de la biblioteca OpenAI Python.

Se espera que las estadísticas sean breves (alrededor de un párrafo) y no deben hacer referencia a los datos directos proporcionados ("Un cliente dice que..." no es el comportamiento esperado).

Este es un ejemplo exitoso. Las reseñas de los clientes son reales, obtenidas de una ubicación de McDonald's en_Mapas de Google._

-   Inmediato:

    -   Sistema:`You are an Executive Assistant.`
    -   Usuario:

```plaintext
Write the manager a quick overview of current business situation shorter than 100 words based on this customer reviews:

- Open 24 hours a day so there is no rush to get there before closing time. Staff are always polite and friendly despite looking incredibly busy looking after drive through, in house and online orders. Old favourites and seasonal options are available on the menu and there is a growing vegan menu which is great to see.],

- Service was good using the drive through.
I can only imagine the staff preparing the food was just about to quit  or get sacked as the cheeseburgers had the cheese on the outside of the bun and the Big Macs had no meat in them at all?????? Too far away to go back, really disappointed and hungry.

- When collecting my meal this week this restaurant was packed and extremely busy the workers who was working on Friday around 18.30 are a credit to you not only was they under very high demanding pressure they stayed calm, polite and professional well done to each one of you 👏 and to top it off even managed to help me with my order back to my vehicle as it was a large order I hope your managers read this and know how good there staff are they will go far in life see you again soon
```

-   Respuesta:

```plaintext
Overall, customer reviews for the business are positive with customers praising the 24-hour service and friendly staff. However, there have been some negative reviews regarding food quality. Despite this, the restaurant remains busy and workers have been commended for their professionalism and ability to handle high-pressure situations.
```

### TODO: Odoo app

Hasta ahora, he estado desarrollando cada paso en una aplicación web simple usando[Matraz](https://flask.palletsprojects.com/en/2.3.x/), que fue suficiente para probar las llamadas API y la autorización OAuth2.0 (que tiene lugar tanto en el lado del cliente como en el del servidor, es decir, en HTML/JS y en la parte Python de Flask). Ahora es el momento de cambiar al marco de Odoo. Cambiar de un sitio web independiente a una aplicación integrada en un ERP acercará el proyecto a la situación comercial real que busco.

-   [ ] Interfaz de usuario: tablero para proporcionar información a primera vista. Tendrá varias tarjetas, cada una para una API de Google. Las tarjetas contendrán:

-   párrafo, el resumen recibido de OpenAI API. Solo se muestra cuando esa API de Google está conectada.

-   botón, para proporcionar la funcionalidad de conectar y desconectar esa API de Google.

## Otros

-   Por qué he elegido un modelo optimizado para chat:
    -   <https://platform.openai.com/docs/guides/chat/chat-vs-completions>
    -   <https://openai.com/pricing#language-models>

### El proceso de refinar el aviso:

TODO: agregue la parte GOOGLE de refining_prompt.md. Explique en primer lugar que pasé reseñas y correos electrónicos a lo largo del aviso.

#### RESTAURANTE

-   Inmediato:
    -   Sistema:`You are an Executive Assistant.`
    -   Usuario:`Write the manager an executive summary shorter than 100 words based on this reviews.`
-   Respuesta:
    ```plaintext
    The restaurant offers 24-hour service with friendly staff and a diverse menu including vegan options. However, one customer experienced poor food quality. Despite this, the workers remained professional and helpful during a busy period.
    ```

pidiendo un`executive summary`nos da información que ya sabemos si somos el administrador del negocio (ej.`The restaurant offers 24-hour service`), sin darle ningún valor a esa información: ¿a los clientes les gusta el servicio 24 horas? Cambiamos`executive summary`para`current customer satisfaction`

-   Inmediato:
    -   Sistema:`You are an Executive Assistant.`
    -   Usuario:`Write the manager quick overview of current customer satisfaction shorter than 100 words based on this reviews.`
-   Respuesta:
    ```plaintext
    Overall, customer satisfaction is high with positive feedback on the 24-hour availability, friendly staff, and diverse menu options including vegan choices. However, there was one negative review regarding incorrect food preparation. Despite this, the majority of customers are pleased with the service and professionalism of the staff during busy periods.
    ```

Ahora el modelo se centra demasiado en los propios clientes (p.`there was one negative review`) Cambiamos`current customer satisfaction`para`current business situation`.

-   Inmediato:
    -   Sistema:`You are an Executive Assistant.`
    -   Usuario:`Write the manager a quick overview of current business situation shorter than 100 words based on this customer reviews.`
-   Respuesta:
    ```plaintext
    Overall, customer reviews for the business are positive with customers praising the 24-hour service and friendly staff. However, there have been some negative reviews regarding food quality. Despite this, the restaurant remains busy and workers have been commended for their professionalism and ability to handle high-pressure situations.
    ```

#### PROVEEDOR DE INTERNET

-   Inmediato:
    -   Sistema:`You are an Executive Assistant.`
    -   Usuario:`Write the manager a quick overview of current business situation shorter than 100 words based on this customer support emails.`

-   Respuesta:

    ```plaintext
    Dear Manager, 
    We have been receiving a mix of customer feedback regarding our internet services. Some customers are experiencing internet connection issues and slow internet speeds, while others are satisfied with the quality of internet provided. We have also received a billing issue complaint and a delayed installation complaint. We need to address these issues promptly to maintain customer satisfaction. 
    Best regards, 
    Executive Assistant
    ```

    Ahora le decimos al modelo que`Avoid headers and signatures like "Dear Manager"`. A veces la modelo los produce, quizás por la seriedad y profesionalidad del System Prompt:`You are an Executive Assistant.`

-   Inmediato:
    -   Sistema:`You are an Executive Assistant.`
    -   Usuario:`Write the manager a quick overview of current business situation shorter than 100 words based on this customer support emails. Avoid headers and signatures like "Dear Manager".`

-   Respuesta:
    ```plaintext
    Customers are facing internet connection issues such as frequent disconnection, slow internet speeds, and delayed installation. Additionally, one customer has raised concerns about their billing. However, one customer has expressed their satisfaction with the quality of internet and customer service. Immediate action is required to address the issues faced by the customers.
    ```
