import os
import time

import openai
from .utils import beautify


def _create(prompt, system_prompt="You are a helpful assistant."):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    max_retries = 10  # Maximum number of retries
    base_delay = 1  # Initial delay in seconds
    backoff_factor = 2  # Delay multiplication factor

    for retry_attempt in range(max_retries + 1):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"{system_prompt}"},
                    {"role": "user", "content": f"{prompt}"},
                ],
            )
            return response["choices"][0]["message"]["content"]
        except openai.error.RateLimitError:  # That model is currently overloaded with other requests
            if retry_attempt < max_retries:
                delay = base_delay * (backoff_factor**retry_attempt)
                time.sleep(delay)

    return "OpenAI API is currently overloaded. Please try again later."


def translate(texts, language="English"):
    """
    text: list of strings or a string
    language: language to translate to
    """
    if isinstance(texts, list):
        text = beautify(texts)

    prompt = f"Translate non-{language} text into {language} while keeping {language} text unchanged:\n\n{text}"
    translation = _create(prompt)
    return translation


def summarize(texts, text_type="reviews"):
    """
    texts: list of strings or a string. Make sure to call ``translate()`` first if the texts are not in English
    """
    if isinstance(texts, list):
        texts = beautify(texts)

    prompt = f"Write the manager a quick overview of current business situation shorter than 100 words based on this {text_type}. Avoid headers and signatures like 'Dear Manager,':"
    prompt += texts
    summary = _create(prompt, system_prompt="You are an Executive Assistant.")
    return summary
