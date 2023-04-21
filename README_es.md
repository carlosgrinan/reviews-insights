# Integración de la API OpenAI con múltiples plataformas de Google para generar insights sobre el feedback de los clientes.

El objetivo de este proyecto es desarrollar un módulo basado en IA integrado en un sistema ERP-CRM (por determinar) que proporcione un breve resumen sobre la opinión de los clientes.

## Herramientas
- Para obtener la opinión de los clientes, se utilizarán varias API de plataformas de Google:
    - **Perfiles de empresa API**: para obtener opiniones de clientes de *Google Maps* y *Google Search*.
    - **API de lugares**: para obtener opiniones de clientes de *Google Maps*.
    - **API de Gmail**: para obtener correos electrónicos de clientes, como solicitudes de asistencia, de *Gmail*.
    - **API para desarrolladores de Google Play**: para obtener reseñas de aplicaciones de Google Play Store.
    - **API de datos**: para obtener comentarios sobre vídeos de *Youtube*.
    - Para determinar

- Para obtener un resumen significativo de la información, se utilizará GPT-3.5 a través de OpenAI API. 

## Motivación
Los costes asociados a las revisiones y clasificaciones humanas de datos basados en texto hacen que a menudo se dejen de lado en favor de los datos numéricos, que pueden analizarse automáticamente en plataformas como Google Analytics. 

Los recientes avances y la mayor accesibilidad de los modelos generativos lingüísticos de IA han hecho posible automatizar también el análisis de la información basada en texto.

Combinando el análisis de ambos tipos de datos, las empresas pueden obtener información más completa que incorporar a su toma de decisiones.  

Para poner en marcha este proyecto, nos centraremos en el análisis de las opiniones de los clientes. Sin embargo, el mismo enfoque puede aplicarse a otros tipos de datos valiosos basados en texto.

Traducción realizada con la versión gratuita del traductor www.DeepL.com/Translator