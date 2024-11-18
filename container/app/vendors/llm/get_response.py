"""Get a response from the LLM."""

import tiktoken
from ...config.logging import logger
from .together import get_response as get_response_together
from .openai import get_response as get_response_openai


def get_response(prompt, quality="fast"):
    """Get a response from the LLM."""
    token_count = count_tokens(prompt)

    logger.info("Token count: %s", token_count)

    # if token_count > 131072:
    #     logger.info("Using OpenAI model, quality: %s", quality)
    #     response = get_response_openai(prompt, quality)
    # else:
    #     logger.info("Using Together model, quality: %s", quality)
    response = get_response_together(prompt, quality)
    return response


def count_tokens(text, model_name="text-davinci-003"):
    """Count the number of tokens in a given text"""
    encoder = tiktoken.encoding_for_model(model_name)

    # Encode the text to get the tokens
    tokens = encoder.encode(text)

    # Return the number of tokens
    return len(tokens)
