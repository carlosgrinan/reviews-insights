Proyecto de Carlos Alejandro Griñán Espada, alumno de segundo curso de DAM del CIFP Carlos III, Cartagena, 2023
- [Introducción](#introducción)
  - [Motivación](#motivación)
  - [Descripción](#descripción)
  - [Demo](#demo)
- [Documentación / memoria técnica descriptiva](#documentación--memoria-técnica-descriptiva)
  - [Tecnologías que se han empleado](#tecnologías-que-se-han-empleado)
    - [Retroalimentación de clientes](#retroalimentación-de-clientes)
    - [Resúmenes de la retroalimentación](#resúmenes-de-la-retroalimentación)
    - [Integración en Odoo](#integración-en-odoo)
  - [Dificultades encontradas y decisiones al respecto](#dificultades-encontradas-y-decisiones-al-respecto)
    - [Optimización](#optimización)
    - [Datos simulados](#datos-simulados)
    - [APIs de Business Profile](#apis-de-business-profile)
    - [Internacionalización](#internacionalización)
    - [Refinando el prompt](#refinando-el-prompt)
      - [Resultado](#resultado)
      - [Proceso](#proceso)
- [Manual de usuario](#manual-de-usuario)
  - [Instalación](#instalación)
  - [Uso](#uso)

# Introducción
**Review Insights** es una app de [Odoo](https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started.html) que ofrece breves resúmenes generados por IA sobre retroalimentación[^1] de clientes obtenida de varios servicios de Google. Está destinada a managers de negocios que quieran 

## Motivación

Históricamente, los análisis de datos basados en texto (como las reseñas de clientes) han requerido revisiones, clasificaciones y resúmenes manuales, con el consecuente coste asociado. Por lo que a menudo se han ignorado en favor de datos numéricos, que pueden analizarse automáticamente en plataformas como *Google Analytics*.

Los avances recientes y la mayor accesibilidad de los modelos de lenguaje de IA han permitido que también sea posible automatizar el análisis de información basada en texto. En el caso concreto de la satisfacción del cliente, ya no somos capaces únicamente de generar gráficos con la puntuación de sus valoraciones, sino que podemos hacer uso de sus opiniones y quejas sin necesidad de revisarlas una a una, de la misma manera que no se revisan las puntuaciones una a una.

Combinando análisis de ambos tipos de datos, las empresas pueden conseguir una visión más completa de su situación, lo que mejora su toma de decisiones.

Esta app se centra en el análisis de retroalimentación de clientes, pero el mismo enfoque puede ser apicado a numerosos tipos de datos basados en texto que posean valor empresarial.

## Descripción

La app genera resumenes utilizando una IA partir de:

* Reseñas de un negocio a elegir de Google Maps
* Emails de tu cuenta de Gmail
* Reseñas de tu negocio de Business Profile [^2]
* Reseñas de tu app en Google Play Store

Una vez hayamos conectado alguno de los servicios anteriores, la app nos ofrecerá un resumen, que se actualiza cada hora con la retroalimentación más reciente.

## Demo

https://github.com/carlosgrinan/proyecto_dam/assets/99912558/7adf24e8-97ed-4434-828e-db3800257701

# Documentación / memoria técnica descriptiva

## Tecnologías que se han empleado

### Retroalimentación de clientes

Se utilizan varias [APIs de Google](https://developers.google.com/apis-explorer) mediante el [Cliente Python de las APIs de Google ](https://github.com/googleapis/google-api-python-client):

- APIs que necesitan autorización del usuario[^3]:
  - **[API de Gmail](https://developers.google.com/gmail/api/guides)**: para obtener emails de *Gmail* (por ejemplo, los recibidos por el departamento de atención al cliente).
  - **[APIs de Business Profile](https://developers.google.com/my-business/content/overview?hl=es)**: para obtener reseñas del negocio de *Google Maps*.
  - [API de Google Play Developer](https://developers.google.com/android-publisher?hl=es-419): para obtener reseñas de la app del negocio de  *Google Play Store*.
  - ~~**[Data API](https://developers.google.com/youtube/v3?hl=es-419)**: para obtener comentarios en videos de*Youtube* del negocio.~~
- No necesitan autorización:
  - **[Places API](https://developers.google.com/maps/documentation/places/web-service/overview)**: para obtener reseñas del negocio de *Google Maps*. Nota: esta API no funciona con el *Cliente Python de las APIs de Google*  y necesita su propio [cliente](https://github.com/googlemaps/google-maps-services-python).

Para obtener la autorización del usuario:

1. [ Librería JavaScript de autorización de terceros de Google](https://developers.google.com/identity/oauth2/web/guides/load-3p-authorization-library) se utiliza para obtener el código de autorización.
2. El código se intercambia por un [token](https://developers.google.com/identity/protocols/oauth2/web-server#httprest_3). [^4]
3. [google-auth](https://googleapis.dev/python/google-auth/latest/user-guide.html) crea *Credenciales*[^5] a partir del token. Las *Credenciales* son utilizadas por el *Cliente Python de las APIs de Google* para acceder a las APIs de Google.

### Resúmenes de la retroalimentación

Se utiliza el modelo de lenguaje [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5)[^6] de la [API de OpenAI](https://platform.openai.com/docs/introduction/overview) mediante la [Libreria Python de OpenAI](https://github.com/openai/openai-python).

### Integración en Odoo

He seguido la arquitectura estándar recomendada en Odoo 16, con la única particularidad del módulo *Job Queue*, que permite crear tareas asíncronas:

- Frontend:

  - [Framework OWL](https://www.odoo.com/documentation/16.0/es/developer/reference/frontend/owl_components.html?highlight=owl)
  - [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/) para el diseño y estructura de la UI.
- Proxy inverso [Nginx](https://nginx.org/)
- Backend:

  - Módulo Base
  - Módulo Web
  - Módulo [Job Queue](https://apps.odoo.com/apps/modules/16.0/queue_job/)
- Base de Datos:

  - [PostgreSQL](https://www.postgresql.org/)

![Arquitectura](https://github.com/carlosgrinan/reviews-insights/assets/99912558/779252d0-59a9-4a5d-b330-c8cf016a9300)


## Dificultades encontradas y decisiones al respecto

### Optimización

El proceso de generación del resumen es bastante lento, pues involucra numerosas llamadas a APIs externas. Puede alcanzar los 30 segundos, incluso con una buena conexión a internet. Hacer esperar al usuario durante tanto tiempo supone una mala experiencia. Por lo tanto, la generación del resumen debe ser asíncrona para permitir al usuario utilizar tanto la app como el resto de Odoo durante ese tiempo.

Comportamiento asíncrono deseado:

1. Cuando el usuario entra en la app, se muestran los resúmenes desactualizados (si los hay)
2. En ese momento se empiecen a generar nuevos resúmenes con la retroalimentación más reciente.
3. Cuando un resumen se haya generado, debería sustituir al antiguo en la UI.

Para lograr la asincronía tanto en el frontend como en el backend he realizado los siguientes pasos:

1. Cuando el usuario entra en la app, es decir, el cliente web manda una petición, en el servidor, un proceso se encarga de responder al cliente web con el resumen antiguo mientras que otro, de manera asíncrona, se encarga de generar el resumen. Para habilitar este **multiprocesamiento** en Odoo, es necesario configurar un proxy inverso *Nginx* (un servidor intermedio entre el cliente web y el servidor) que se encarge de redirigir las peticiónes a los distintos puertos utilizados por el servidor de Odoo.
2. Para poder crear el nuevo proceso asíncrono que se encargue de generar el resumen, necesitamos el módulo *Job Queue* (cola de trabajo). El multiprocesamiento estándar de Odoo está únicamente destinado a asignar distintos procesos a cada uno de los clientes web (o usuarios) conectados, no permite crear procesos asíncronos a partir de un proceso, que es lo que buscamos.
3. Una vez el proceso asíncrono de generación del resumen haya terminado, el resumen debería "enviarse" al cliente web. Teniendo en cuenta las limitaciones de HTTP, hago uso de polling[^7]: cada cierto tiempo, el cliente web envía una nueva petición al servidor preguntando si ya se ha generado el resumen.
4. Cuando el resumen haya llegado definitivamente al cliente web, la "tarjeta" en la que se va a mostrar debe actualizarse. Ahí entra en escena el *Framework OWL.*  Es el framework web creado por Odoo: similar a *React*, es un framework web (JavaScript) basado en componentes reactivos, es decir, la UI está compuesta por elementos que tienen un estado. Cuando el estado cambia, por ejemplo, la variable *resumen* cambia, el componente tipo "tarjeta" que utilizo se renderiza de nuevo sin suponer una perturbación para el resto de la UI. Es un paso más allá de la programación basada en eventos porque los eventos ya se suscriben internamente por el propio framework.

### Datos simulados

No soy dueño de ninguna app de *Google Play Store*  ni poseo un negocio en *Business Profile* por lo que para probar el funcionamiento de sus respectivas APIs he utilizado la clase [HttpMock](https://googleapis.github.io/google-api-python-client/docs/mocks.html) que ofrece el [Cliente Python de las APIs de Google](https://github.com/googleapis/google-api-python-client). Permite especificar un documento en formato *json* con la respuesta que supuestamente recibiríamos de la API. Por ejemplo, cuando solicito las reseñas de una app a la *API de Google Play Developer*  con la siguiente llamada: `service.reviews().list(packageName=package_name, maxResults=10, translationLanguage="en", fields="reviews/comments/userComment/text")`, especifico esta respuesta simulada:

```json
{
    "reviews": [
        {
            "comments": [
                {
                    "userComment": {
                        "text": "This is a review obtained from the Telegram app in Play Store: it has helped me connect with serveral people across the world. May I suggest some quality of life improvements for the app, one, working audio for screen sharing, me and a friend of mine are music producers, and like to show each other what our progress is. it would be convenient to listen while sharing. Also the ability to group chats/ groups. My friend has music groups he is joined in, and it would be nice to have them in a group to seperate personal/business."
                    }
                },
		...,
		]
	}
}
```

Nota: estos datos simulados estan únicamente destinados al proceso de desarrollo. He decidido no incluír datos de demostración de cara al usuario final, puesto que entiendo los mismos como una herramienta para que el usuario pruebe las distintas acciones que puede realizar con ellos. En esta app, el usuario no puede realizar acciones con los datos. Encontrarse con párrafos de ejemplo al iniciar la app únicamente provocaría confusión al usuario, que no tendría claro qué servicios están conectados y cuáles no, dado que todos presentan texto. Para ver el resultado al conectar los servicios, puede referirse al [vídeo de demostración](introduccion.md#demo).

### APIs de Business Profile

Las APIs de Business Profile son APIs privadas. Para poder utilizarlas es necesario [solicitar acceso](https://developers.google.com/my-business/content/prereqs?hl=es#request-access), el cual no he podido obtener porque Google solo se lo otorga a empresas y consultoras de informática reales.

### Internacionalización

La retroalimentación puede estar en distintos idiomas. No obstante, el modelo de lenguaje *gpt-3.5-turbo* ofrece mejores resultados cuando recibe y produce texto en inglés.

He optado por traducir la retroalimentación a inglés antes de enviársela a la API de OpenAI para que la resuma. Para la traducción he utilizado el mismo modelo de lenguaje. Es decir, *gpt-3.5* se encarga de traducir a inglés la información que luego va a tener que resumir. De esta manera los resultados son mejores que encargándole la tarea de resumir (en inglés) textos de distintos idiomas.

Además, ya generado el resumen en inglés, si el usuario está utilizando Odoo en un idioma distinto, se envía de nuevo para que *gpt-3.5* lo traduzca, por ejemplo a español.

Otra opción habría sido utilizar un servicio específico de traducción, como *DeepL*, pero los resultados son [similares ](https://blog.inten.to/chatgpt-for-translation-surpassing-gpt-3-e8e34f37befb)y la interfaz con la API de OpenAI ya está montada.

### Refinando el prompt

Los resúmenes de la retroalimentación deben ser cortos (no más de un párrafo) y no deben referirse directamente a los datos concretos de la retroalimentación (por ejemplo, "*un cliente dice que...*" no es el comportamiento deseado).

#### Resultado

Este en un ejemplo exitoso. La retroalimentación consiste en reviews reales, obtenidas de un McDonald's de *Google Maps*.

Nota: prompts y resultados traducidos al español, pueden verse los originales en inglés [aquí](./docs/prompt_refining.md), junto con más ejemplos del proceso de refinamiento.

- Prompt:

  * [Sistema](https://platform.openai.com/docs/api-reference/chat/create#chat/create-role): `Eres un asistente ejecutivo.`
  * Usuario:

```plaintext
Escríbele al manager un resumen de la situacion actual del negocio de menos de 100 palabras basado en estas reseñas:

- Abierto las 24 horas del día por lo que no haya prisa por llegar antes de la hora de cierre. El personal siempre es educado y amable a pesar de parecer increíblemente ocupado cuidando de los pedidos en coche, en casa y en línea. Los viejos favoritos y las opciones de temporada están disponibles en el menú y hay un menú vegano en crecimiento que es genial de ver.

- El servicio fue bueno usando el coche.
Imagino que el personal que preparaba la comida estaba a punto de dimitir o ser despedido ya que las hamburguesas con queso tenían el queso en el exterior del pan y los Big Mac no tenían carne en absoluto. Demasiado lejos para volver, realmente decepcionado y hambriento.

- Cuando recogí mi comida esta semana, este restaurante estaba lleno y extremadamente ocupado, los trabajadores  del viernes alrededor de las 18:30 no solo estaban bajo una presión muy exigente, se mantuvieron tranquilos, educados y profesionales. usted 👏 y para colmo, incluso logró ayudarme con mi pedido de regreso a mi vehículo, ya que era un pedido grande. Espero que sus gerentes lean esto y sepan lo bueno que es el personal. Llegarán lejos en la vida. Nos vemos pronto.
```

- Respuesta:

```plaintext
En general, las reseñas de los clientes sobre el negocio son positivas y los clientes elogian el servicio las 24 horas y el amable personal. Sin embargo, ha habido algunas críticas negativas sobre la calidad de la comida. A pesar de esto, el restaurante sigue ocupado y se ha elogiado a los trabajadores por su profesionalismo y capacidad para manejar situaciones de alta presión.
```

#### Proceso

- Prompt:
  - Sistema: `Eres un asistente ejecutivo.`
  - Usuario: `Escríbele al manager un resumen ejecutivo de menos de 100 palabras basado en estas reseñas.`
- Respuesta:
  ```plaintext
  El restaurante ofrece servicio 24 horas con
  El restaurante ofrece servicio las 24 horas con un personal amable y un menú variado que incluye opciones veganas. Sin embargo, un cliente experimentó una comida de mala calidad. A pesar de esto, los trabajadores se mantuvieron profesionales y serviciales durante un período ajetreado.
  ```

Al pedir un `resumen ejecutivo` nos da información obvia que deberíamos conocer si somos el manager del negocio (por ejemplo `El restaurante ofrece servicio 24 horas`), sin añadir ningún valor a esa información (¿A los clientes les gusta el servicio 24 horas?). Cambio  `resumen ejecutivo` por `satisfacción actual de los clientes`

- Prompt:
  - Sistema: `Eres un asistente ejecutivo.`
  - Usuario: `Escríbele al manager un resumen de la satisfacción actual de los clientes de menos de 100 palabras basado en estas reseñas.`
- Respuesta:
  ```plaintext
  En general, la satisfacción del cliente es alta con comentarios positivos sobre la disponibilidad las 24 horas, el personal amable y las diversas opciones de menú, incluidas opciones veganas. Sin embargo, hubo una reseña negativa con respecto a la preparación incorrecta de alimentos. A pesar de esto, la mayoría de los clientes están satisfechos con el servicio y la profesionalidad del personal durante los períodos de mayor actividad.
  ```

Ahora la IA se centra demasiado en los clientes (`hubo una reseña negativa`). Cambio `satisfacción actual de los clientes` for `situación actual del negocio`.

- Prompt:
  * Sistema: `Eres un asistente ejecutivo.`
  * Usuario: `Escríbele al manager un resumen de la situación actual del negocio de menos de 100 palabras basado en estas reseñas.`
- Respuesta:
  ```plaintext
  En general, las reseñas de los clientes sobre el negocio son positivas y los clientes elogian el servicio las 24 horas y el amable personal. Sin embargo, ha habido algunas críticas negativas sobre la calidad de la comida. A pesar de esto, el restaurante sigue ocupado y se ha elogiado a los trabajadores por su profesionalismo y capacidad para manejar situaciones de alta presión.
  ```
## Flujo de datos y funcionalidad
### Entrar
<img src="https://github.com/carlosgrinan/reviews-insights/assets/99912558/12b54faa-c939-4d90-846e-861bcbb1b9d8" width=50% height=50%>

### Conectar
![Conectar](https://github.com/carlosgrinan/reviews-insights/assets/99912558/485ac4eb-dcd4-467b-9a7a-f676768a3f41)


### Desconectar
<img src="https://github.com/carlosgrinan/reviews-insights/assets/99912558/9e29f108-d044-40fc-8f19-223b706febdc" width=50% height=50%>


# Manual de usuario

## Instalación

1. Clona el [repositorio](https://github.com/carlosgrinan/reviews_insights) de la app dentro del directorio `addons` de tu instalación de Odoo 16.
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
5. Sustituye el `client_id` especificado en `reviews_insights/static/src/card/card.js` por tu *Client ID* de Google (el que has añadido al fichero `.env`).
6. Habilitar el [multiprocesamiento ](https://www.odoo.com/documentation/16.0/administration/install/deploy.html#builtin-server)en Odoo, mediante la [configuración estándar](https://www.odoo.com/documentation/16.0/administration/install/deploy.html#https) recomendada (un proxy inverso *nginx*).

## Uso

Puedes ver una demostración [aquí](introduccion.md#demo).

1. Introduce el [identificador de tu negocio](https://developers.google.com/maps/documentation/places/web-service/place-id#find-id) (Google Maps) o el del [paquete de tu app](https://developer.android.com/studio/build/application-id?hl=es-419) (Google Play Store).
2. Pulsa el botón "conectar".
3. En unos segundos se generará el resumen.
4. Para desconectar el servicio, pulsa en "desconectar".

[^1]: Reseñas, comentarios, emails (por ejemplo, los recibidos por la cuenta de soporte técnico de un negocio)... En resumen, información que arroje luz sobre la situación actual del negocio en cuanto a satisfacción del cliente.
    
[^2]: Las reseñas de *Maps* y *Business Profile* son la  mismas. Si conectamos *Maps*, el resumen se generará a partir de un máximo de 5 reseñas, mientras que con *Business Profile* no existe esta limitación, por lo que el resumen será de mayor calidad. No obstante, *Business Profile* requiere autorización, por lo que debemos tener la propiedad del negocio. Para beneficiarnos de ambos, recomendamos conectar *Business Profile* para obtener un resumen de nuestro negocio, y conectar *Maps* a un negocio tercero en el que estemos interesados, por ejemplo, un negocio de la competencia.

[^3]: Las APIs de Google que ofrecen recursos protegidos  requieren autorización del propietario de los mismos (el usuario) mediante el protocolo OAuth2.0, aunque solamente se acceda a recursos abiertos al público (como las reseñas de las *APIs de Business Profile*).
    
[^4]: Existe una librería específica para esto: [google-auth-oauthlib](https://google-auth-oauthlib.readthedocs.io/en/latest/). Pero creo que añade complejidad innecesaria por lo que he optado por utilizar la librería estándar HTTP [requests](https://requests.readthedocs.io/en/latest/).
    
[^5]: Las Credenciales encapsulan los token y otros datos necesarios. *google-auth* se encarga de solicitar automáticamente un nuevo token de acceso cuando caduca.
    
[^6]: La app no utiliza la capacidad de recordar mensajes que tiene este modelo optimizado para chat. Lo he escogido simplemente porque [su rendimiento es similar al de otros como davinci pero a un precio inferior](https://platform.openai.com/docs/guides/chat/chat-vs-completions).
    
[^7]: Una mejor solución es hacer uso de websocket, para establecer una conexión permanente entre cliente y servidor. No obstante, esta característica fue introducida muy recientemente en Odoo 16 por lo que la documentación es muy escasa.
    

