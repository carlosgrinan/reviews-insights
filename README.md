# Integration of OpenAI API with multiple Google APIs for generating customer feedback insights

The objective of this project is to develop an Odoo module that provides AI-powered short summaries on customer feedback.

## Tools

- To obtain customer feedback, various Google APIs will be used:
  - **Business Profile APIs**: to obtain customer reviews from *Google Maps* and *Google Search*.
  - **[Places API](https://developers.google.com/maps/documentation/places/web-service/overview)**: to obtain customer reviews from *Google Maps*.
  - **Gmail API**: to obtain customer emails, such as support requests, from *Gmail*.
  - **Google Play Developer API**: to obtain app reviews from *Google Play Store*.
  - **Data API**: to obtain comments on videos from *Youtube*.
  - To be determined
- To obtain insights (summary and tips) on the information, a Language Generative model (like GPT-3.5) will be used through OpenAI API.

## Motivation

The costs associated with human reviews and classifications of text-based data often lead to its neglect in favor of numerical data, which can be automatically analyzed on platforms like Google Analytics.

The recent advancements and increased accessibility of AI Language Generative models have made it possible to automate the analysis of text-based information too.

By combining analyses of both types of data, companies can gain more comprehensive insights which to incorporate into their decision-making.

To kickstart this project, our focus will be on analyzing customer feedback. However, the same approach can be applied to other types of valuable text-based data.

## Milestones

1. **[Authorization](#authorization)**: Implement an authorization flow using the OAuth 2.0 protocol to access the protected resources of the Google APIs.
2. **Configurate a developer account** to access the APIs of the Google Cloud Platform and OpenAI.
3. **Data requests and collection**:

   - Define the requests to be made to the Google platforms' APIs.
   - Define the requests to be made to OpenAI API.
     - Choose a suitable OpenAI model.
     - Define the prompt.
4. **Data processing**:

   - Process the response data from the Google platforms' APIs to fit the requests of the OpenAI API.
   - Process the response data from the OpenAI API to obtain the customer feedback summary.
5. **Odoo app**:

   - Provides configuration options for the user, and a way to initiate the authorization flow.
   - Show the customer feedback summary to the user.

### Authorization

To access sensitive data as a 3rd party application, we need authorization from the user.

### Odoo app

UI: dashboard to provide info at first-glance. It will have multiple cards, each one for a Google API. The cards will contain:

* paragraph, the summary received from OpenAI API. Only shown when that Google API is connected.
* button, to provide the functionality of connecting and disconnecting that Google API.

Models:




Referencia OpenAi para presentación

* Por qué he elegido un modelo de chat:
  * https://platform.openai.com/docs/guides/chat/chat-vs-completions
  * https://openai.com/pricing#language-models
