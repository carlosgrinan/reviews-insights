# Review Insights

**Review Insights** es una app de [Odoo](https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started.html) que ofrece breves resúmenes generados por IA sobre retroalimentación[^1] de clientes obtenida de varios servicios de Google.

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

[^1]: Reseñas, comentarios, emails (por ejemplo, los recibidos por la cuenta de soporte técnico de un negocio)... En resumen, información que arroje luz sobre la situación actual del negocio en cuanto a satisfacción del cliente.
    
[^2]: Las reseñas de *Maps* y *Business Profile* son la  mismas. Si conectamos *Maps*, el resumen se generará a partir de un máximo de 5 reseñas, mientras que con *Business Profile* no existe esta limitación, por lo que el resumen será de mayor calidad. No obstante, *Business Profile* requiere autorización, por lo que debemos tener la propiedad del negocio. Para beneficiarnos de ambos, recomendamos conectar *Business Profile* para obtener un resumen de nuestro negocio, y conectar *Maps* a un negocio tercero en el que estemos interesados, por ejemplo, un negocio de la competencia.
