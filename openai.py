import openai
import os


def summarize(texts, type_of_text="reviews"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Write the manager a quick overview of current business situation shorter than 100 words based on this {type_of_text}. Avoid headers and signatures like 'Dear Manager,':"
    prompt += texts.__str__()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an Executive Assistant."},
            {"role": "user", "content": f"{prompt}"},
        ],
    )
    summary = response["choices"][0]["message"]["content"]
    return summary
