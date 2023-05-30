import os
import openai
import time


def create(prompt, system_prompt="You are a helpful assistant."):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    max_retries = 10  # Maximum number of retries
    base_delay = 1  # Initial delay in seconds
    backoff_factor = 2  # Delay multiplication factor

    for retry_attempt in range(max_retries + 1):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{system_prompt}"},
                {"role": "user", "content": f"{prompt}"},
            ],
        )

        if "choices" in response:
            return response["choices"][0]["message"]["content"]
        else:
            if retry_attempt < max_retries:
                delay = base_delay * (backoff_factor**retry_attempt)
                time.sleep(delay)

    return None


def translate(text, language="English"):
    prompt = f"Translate non-{language} text into {language} while keeping {language} text unchanged:\n\n{text}"
    translation = create(prompt)
    return translation


def summarize(texts, text_type="reviews"):
    if texts:
        text = "- " + "\n\n- ".join(texts)

        # Translate to English to get better results
        text = translate(text)
        # print("Translated text:")
        # print(text)

        prompt = f"Write the manager a quick overview of current business situation shorter than 100 words based on this {text_type}. Avoid headers and signatures like 'Dear Manager,':"
        prompt += text
        summary = create(prompt, system_prompt="You are an Executive Assistant.")
        print("Summary:")
        print(summary)
        return summary

    else:
        return "No hay suficientes datos para generar un resumen. Por favor, conecta otra cuenta."
