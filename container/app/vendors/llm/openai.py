"""Get a response from the OpenAI model."""

from ...config.logging import logger
from openai import OpenAI, OpenAIError

client_openai = OpenAI()


def get_response(prompt, quality="fast"):
    """Use the OpenAI model to get a response, skipping internal retries."""
    try:
        if quality == "fast":
            model = "gpt-4o-mini"
        else:
            model = "gpt-4o-latest"
        response = client_openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        logger.error("Error using OpenAI model: %s", e)
        return None
