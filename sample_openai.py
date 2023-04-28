import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Retrieve the value of the "foo" variable
foo = os.getenv("OPENAI_API_KEY")

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7
)


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {
            "role": "assistant",
            "content": "The Los Angeles Dodgers won the World Series in 2020.",
        },
        {"role": "user", "content": "Where was it played?"},
    ],
)

summary = response["choices"][0]["message"]["content"]
print(summary)
