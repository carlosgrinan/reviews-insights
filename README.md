# Integration of OpenAI API with multiple Google APIs for generating customer feedback insights

The objective of this project is to develop an [Odoo](https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started.html) app that provides AI-powered brief insights on customer feedback.

## Motivation

The costs associated with human reviews and classifications of text-based data often lead to its neglect in favor of numerical data, which can be automatically analyzed on platforms like Google Analytics. The recent advancements and increased accessibility of AI Language Generative models have made it possible to automate the analysis of text-based information too. By combining analyses of both types of data, companies can gain more comprehensive insights which to incorporate into their decision-making.
To kickstart this project, our focus will be on analyzing customer feedback. However, the same approach can be applied to other types of valuable text-based data.

## Tools

- To obtain customer feedback, various [Google APIs](https://developers.google.com/apis-explorer) will be used through [Google API Client](https://github.com/googleapis/google-api-python-client):

  - Need Oauth2.0 authorization:
    - **[Gmail API](https://developers.google.com/gmail/api/guides)**: to obtain customer support emails from *Gmail*.
    - TODO: **Business Profile APIs**: to obtain customer reviews from *Google Maps* and *Google Search*.
    - TODO: **Google Play Developer API**: to obtain app reviews from *Google Play Store*.
    - TODO: **Data API**: to obtain comments on videos from *Youtube*.
  - Don't need authorization (publicly available data):
    - **[Places API](https://developers.google.com/maps/documentation/places/web-service/overview)**: to obtain up to 5 reviews from a *Google Maps* place. Note that this API doesn't work with Google API Client and needs its own [client](https://github.com/googlemaps/google-maps-services-python)
- To obtain user consent to access protected resources from the Google APIs that require Oauth2.0 authorization:

  1. [Google 3P Authorization JavaScript Library](https://developers.google.com/identity/oauth2/web/guides/load-3p-authorization-library) will be used to obtain an authorization code
  2. The authorization code will be exchanged for a [token](https://developers.google.com/identity/protocols/oauth2/web-server#httprest_3). I've found [google-auth-oauthlib](https://google-auth-oauthlib.readthedocs.io/en/latest/) to overcomplicate the task so I've opted for a simple HTTP request.
  3. [google-auth](https://googleapis.dev/python/google-auth/latest/user-guide.html) will be used to create Credentials from the token. The Credentials will be used by the aforementioned Google API Client to access Google APIs.
- To obtain insights (summary and/or tips) on the information, the language model [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5) from [OpenAI API](https://platform.openai.com/docs/introduction/overview) will be used through the [OpenAI Python library](https://github.com/openai/openai-python).
- TODO: Odoo

  - The frontend will use [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/).

## Milestones

### Obtaining customer feedback

* [X] Configurate a developer account to access Google APIs.
* [X] Obtain publicly available data from a Google API (reviews from Places API).
* [X] Obtain protected resources from a Google API (emails from Gmail API).

### Obtaining insights

* [X] Configurate a developer account to access OpenAI API.
* [X] Refining the prompt. This step took place on [OpenAI Playground](https://platform.openai.com/playground) to focus on the prompt and response.
* [X] Obtain insights through the OpenAI Python library.

Insights are expected to be short (around a paragraph's length), and shouldn't make reference to the direct data provided ("One customer says that..." is not the expected behaviour).

This is a succesful example. Customer reviews are real, obtained from a McDonald's location in *Google Maps.*

- Prompt:

  * System: `You are an Executive Assistant.`
  * User:

```plaintext
Write the manager a quick overview of current business situation shorter than 100 words based on this customer reviews:

- Open 24 hours a day so there is no rush to get there before closing time. Staff are always polite and friendly despite looking incredibly busy looking after drive through, in house and online orders. Old favourites and seasonal options are available on the menu and there is a growing vegan menu which is great to see.],

- Service was good using the drive through.
I can only imagine the staff preparing the food was just about to quit  or get sacked as the cheeseburgers had the cheese on the outside of the bun and the Big Macs had no meat in them at all?????? Too far away to go back, really disappointed and hungry.

- When collecting my meal this week this restaurant was packed and extremely busy the workers who was working on Friday around 18.30 are a credit to you not only was they under very high demanding pressure they stayed calm, polite and professional well done to each one of you 👏 and to top it off even managed to help me with my order back to my vehicle as it was a large order I hope your managers read this and know how good there staff are they will go far in life see you again soon
```

- Response:

```plaintext
Overall, customer reviews for the business are positive with customers praising the 24-hour service and friendly staff. However, there have been some negative reviews regarding food quality. Despite this, the restaurant remains busy and workers have been commended for their professionalism and ability to handle high-pressure situations.
```

### TODO: Odoo app

Up until now, I've been developing each step on a simple web application using [Flask](https://flask.palletsprojects.com/en/2.3.x/), which was enough to test API calls and OAuth2.0 authorization (which takes place both on client and server side, i.e. on the HTML/JS and on the Python part of Flask). Now it's time to switch to the Odoo framework. Switching from a standalone website to an app integrated into an ERP will get the project closer to the real business situation that I aim for.

* [ ] UI: dashboard to provide info at first-glance. It will have multiple cards, each one for a Google API. The cards will contain:

* paragraph, the summary received from OpenAI API. Only shown when that Google API is connected.
* button, to provide the functionality of connecting and disconnecting that Google API.

## Others

- Why I've chosen a chat-optimized model:
  - https://platform.openai.com/docs/guides/chat/chat-vs-completions
  - https://openai.com/pricing#language-models

### The process of refining the prompt:

TODO: add the GOOGLE part from refining_prompt.md. Explain firstly that i passed reviews and emails along the prompt.

#### RESTAURANT

- Prompt:
  - System: `You are an Executive Assistant.`
  - User: `Write the manager an executive summary shorter than 100 words based on this reviews.`
- Response:
  ```plaintext
  The restaurant offers 24-hour service with friendly staff and a diverse menu including vegan options. However, one customer experienced poor food quality. Despite this, the workers remained professional and helpful during a busy period.
  ```

Asking for an `executive summary` gives us information that we already know if we are the manager of the business (e.g. `The restaurant offers 24-hour service`), without giving any value to that information: do customers like the 24-hour service? We change `executive summary` for `current customer satisfaction`

- Prompt:
  - System: `You are an Executive Assistant.`
  - User: `Write the manager quick overview of current customer satisfaction shorter than 100 words based on this reviews.`
- Response:
  ```plaintext
  Overall, customer satisfaction is high with positive feedback on the 24-hour availability, friendly staff, and diverse menu options including vegan choices. However, there was one negative review regarding incorrect food preparation. Despite this, the majority of customers are pleased with the service and professionalism of the staff during busy periods.
  ```

Now the model focus too much on the customers themselves (e.g. `there was one negative review`) We change `current customer satisfaction` for `current business situation`.

- Prompt:
  * System: `You are an Executive Assistant.`
  * User: `Write the manager a quick overview of current business situation shorter than 100 words based on this customer reviews.`
- Response:
  ```plaintext
  Overall, customer reviews for the business are positive with customers praising the 24-hour service and friendly staff. However, there have been some negative reviews regarding food quality. Despite this, the restaurant remains busy and workers have been commended for their professionalism and ability to handle high-pressure situations.
  ```

#### INTERNET PROVIDER

- Prompt:
  - System: `You are an Executive Assistant.`
  - User: `Write the manager a quick overview of current business situation shorter than 100 words based on this customer support emails.`
- Response:
  ```plaintext
  Dear Manager, 
  We have been receiving a mix of customer feedback regarding our internet services. Some customers are experiencing internet connection issues and slow internet speeds, while others are satisfied with the quality of internet provided. We have also received a billing issue complaint and a delayed installation complaint. We need to address these issues promptly to maintain customer satisfaction. 
  Best regards, 
  Executive Assistant
  ```

  Now we tell the model to `Avoid headers and signatures like "Dear Manager"`. Sometimes the model produces them, maybe because of the serious and professional nature of the System Prompt: `You are an Executive Assistant.`

- Prompt:
  - System: `You are an Executive Assistant.`
  - User: `Write the manager a quick overview of current business situation shorter than 100 words based on this customer support emails. Avoid headers and signatures like "Dear Manager".`
- Response:
  ```plaintext
  Customers are facing internet connection issues such as frequent disconnection, slow internet speeds, and delayed installation. Additionally, one customer has raised concerns about their billing. However, one customer has expressed their satisfaction with the quality of internet and customer service. Immediate action is required to address the issues faced by the customers.
  ```
