
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
