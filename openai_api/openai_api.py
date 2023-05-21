import os

import openai


def create(prompt, system_prompt="You are a helpful assistant."):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{prompt}"},
        ],
    )
    return response["choices"][0]["message"]["content"]


def translate(text, language="English"):
    prompt = f"Translate non-{language} text into {language} while keeping {language} text unchanged:\n\n{text}"
    translation = create(prompt)
    return translation


def summarize(texts, text_type="reviews"):
    if texts:
        text = "- " + "\n\n- ".join(texts)
        text = translate(text)

        prompt = f"Write the manager a quick overview of current business situation shorter than 100 words based on this {text_type}. Avoid headers and signatures like 'Dear Manager,':"
        prompt += texts.__str__()
        summary = create(prompt, system_prompt="You are an Executive Assistant.")
        return summary

    else:
        return "No hay suficientes datos para generar un resumen. Por favor, conecta otra cuenta."
