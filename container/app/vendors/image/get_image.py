"""Get a response from the LLM."""

from io import BytesIO
import base64
import requests
from ...config.logging import logger
from .generate_image_openai import generate_image_openai
from .generate_image_together import generate_image_together


def get_image(prompt, vendor="together"):
    """Get an image from OpenAI or Together AI, returning a base64 encoded string."""

    logger.info(f"Getting image with vendor: {vendor}")
    if vendor == "together":
        try:
            return generate_image_together(prompt)
        except Exception as e:
            logger.error(f"Error generating image with Together AI: {e}")
    elif vendor == "openai":
        try:
            image_url = generate_image_openai(prompt)
            if image_url:
                return url_to_base64_image(image_url)
        except Exception as e:
            logger.error(f"Error generating image with OpenAI: {e}")
    else:
        logger.error(f"Invalid vendor: {vendor}")


def url_to_base64_image(url):
    """Download image from URL and convert to base64 encoded string."""
    response = requests.get(url)
    response.raise_for_status()
    image_data = response.content
    return f"data:image/png;base64,{base64.b64encode(image_data).decode()}"


# def get_image_url(prompt):
#     """Get a response from the LLM."""
#     try:
#         image_url = generate_image_openai(prompt)
#         logger.info(f"get_image Image URL: {image_url}")
#         return image_url
#     except Exception as e:
#         logger.error(f"Error generating image: {e}")
#         return None
