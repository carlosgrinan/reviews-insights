import os

import googlemaps
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))

response = gmaps.place(
    "ChIJN1t_tDeuEmsRUsoyG83frY4",
    fields=["reviews"],
    language="en",
    reviews_sort="most_relevant",
)
reviews = response["result"]["reviews"]

reviews_texts = [review["text"] for review in reviews]

prompt = "Write the manager a quick overview of current business situation shorter than 100 words based on this reviews:"
prompt += reviews_texts.__str__()
# print(prompt)
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}"},
    ],
)
summary = response["choices"][0]["message"]["content"]
print(summary)
