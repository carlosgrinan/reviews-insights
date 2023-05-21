import os
import openai


def summarize(texts, text_type="reviews"):
    if texts:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Write the manager a quick overview of current business situation shorter than 100 words based on this {text_type}. Avoid headers and signatures like 'Dear Manager,':"
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

    else:
        return "No hay suficientes datos para generar un resumen. Por favor, conecta otra cuenta."
