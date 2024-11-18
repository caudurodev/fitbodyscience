# import uuid  # Import uuid library to generate a unique identifier
# from pathlib import Path
from openai import OpenAI
from ...config.logging import logger

client = OpenAI()


def generate_image_openai(prompt):
    """Generate audio from text using OpenAI's TTS API."""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        logger.info(f"Image generated: {image_url}")
        return image_url
    except Exception as e:
        print(f"Error generating audio from text: {e}")
        return None
