"""Get a response from the OpenAI model."""

from ...config.logging import logger
from openai import OpenAI, OpenAIError

client = OpenAI()


def get_embedding(text):
    """Get an embedding from the OpenAI model."""
    try:
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        return response.data[0].embedding
    except OpenAIError as e:
        logger.error("Error using OpenAI embedding: %s", e)
        return None
