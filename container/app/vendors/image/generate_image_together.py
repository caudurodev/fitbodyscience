"""
This file contains the implementation of the Together model for generating images.
"""

import os
import base64
import json
from io import BytesIO
from PIL import Image
from together import Together
from ...config.constants import TOGETHER_API_KEY
from ...config.logging import logger
import requests

client = Together(api_key=TOGETHER_API_KEY)


def generate_image_together(prompt):
    """Generate an image using the Together AI Stable Diffusion model."""
    try:
        logger.info(f"Generating image for prompt: {prompt[:50]}...")
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1.1-pro",
            steps=10,
            width=1024,
            height=1024,
            n=1,
        )

        # logger.info(f"Raw API response: {json.dumps(response.dict(), indent=2)}")

        if not response.data:
            logger.error("No data in the response")
            return None

        image_data = response.data[0]
        # logger.info(f"Image data: {json.dumps(image_data.dict(), indent=2)}")

        # Check if the response contains a URL
        if hasattr(image_data, "url"):
            # logger.info(f"Image URL: {image_data.url}")
            # Download the image from URL
            image_response = requests.get(image_data.url, timeout=60)
            image_response.raise_for_status()
            image_data_decoded = image_response.content
        elif hasattr(image_data, "b64_json"):
            # Decode the base64 string
            image_data_decoded = base64.b64decode(image_data.b64_json)
        else:
            logger.error("Neither b64_json nor url found in the response")
            return None

        # Create a PIL Image object
        image = Image.open(BytesIO(image_data_decoded))

        # Convert the image to base64 for further processing or storage
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # logger.info(f"Image generated successfully for prompt: {prompt[:50]}...")
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        logger.error(f"Error generating image from prompt: {str(e)}", exc_info=True)
        return None
