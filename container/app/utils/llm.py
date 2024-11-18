import os
import re
import requests
import json
import openai
from together import Together
import time
from datetime import datetime, timedelta
from openai import OpenAI, OpenAIError
from groq import Groq
from ..video.get_transcript_from_video import count_tokens
from ..utils.config import logger, settings

client_openai = OpenAI()
client_groq = Groq()
client_together = Together(api_key=os.environ.get("TOGETHER_API_KEY"))


# Dictionary to store the next allowed request time for each service
next_request_time = {
    "groq": datetime.now(),
    "openai": datetime.now(),
    "together": datetime.now(),
}


def get_response(prompt, model=None, response_format="json"):
    """Get a response from LLM, using Together for shorter prompts and OpenAI for longer prompts."""
    if not prompt:
        logger.error("Error: Invalid empty prompt")
        return None

    token_count = count_tokens(prompt)
    # logger.info("Count tokens in prompt: %s", token_count)

    if not isinstance(prompt, list) or not all(
        isinstance(item, dict) for item in prompt
    ):
        prompt = [{"role": "system", "content": str(prompt)}]

    provider = "openai" if token_count > 4000 else "together"
    services = {
        "together": (use_together_model, ["meta-llama/Llama-3-70b-chat-hf"]),
        "openai": (use_openai_model, ["gpt-4o-2024-05-13"]),
    }

    function, models = services[provider]
    if model is None or model not in models:
        model = models[0]

    try:
        time_start = time.time()
        response = function(prompt, response_format, model)
        time_end = time.time()
        # logger.info(
        #     "Time taken to get response from %s: %s seconds",
        #     provider,
        #     time_end - time_start,
        # )
        return response
    except RateLimitError as e:
        logger.error("Rate limit error: %s", e)
        retry_after = int(e.headers.get("Retry-After", 60))
        next_request_time[provider] = datetime.now() + timedelta(seconds=retry_after)
        logger.error(
            "%s rate limited. Retrying after %s seconds.", provider, retry_after
        )
    except Exception as e:
        logger.error("Error obtaining response from %s: %s", provider, e)

    logger.error("No valid response obtained from LLM provider.")
    return None


def use_openai_model(
    message_history, response_format="json", model="gpt-4o-2024-05-13"
):
    """Use the OpenAI model to get a response, skipping internal retries."""
    request_kwargs = {
        "model": model,
        "messages": message_history,
        "response_format": {"type": "json_object"} if response_format == "json" else {},
    }
    try:
        response = client_openai.chat.completions.create(**request_kwargs)
        completion = response.choices[0].message.content
        return completion
    except OpenAIError as e:
        logger.error("Error using OpenAI model: %s", e)
        if hasattr(e, "response") and e.response.headers:
            logger.error("Error OpenAI rate limit info: %s ", e.response.headers)
            return None, e.response.headers
        return None, None


def use_groq_model(
    message_history, response_format="json", model="llama3-70b-8192", **request_kwargs
):
    """Use the Groq models to get a response."""
    request_kwargs.update(
        {
            "model": model,
            "messages": message_history,
            "response_format": (
                {"type": "json_object"} if response_format == "json" else {}
            ),
        }
    )
    try:
        response = client_groq.chat.completions.create(**request_kwargs)
        completion = response.choices[0].message.content
        return completion
    except Exception as e:
        logger.error("Error using Groq model %s: %s", model, e)
        if hasattr(e, "response") and e.response.headers:
            logger.error("Error Groq rate limit info: %s ", e.response.headers)
            return None, e.response.headers
        return None


def use_together_model(
    message_history,
    response_format="json",
    model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    # model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
    **request_kwargs
):
    """Use the Groq models to get a response."""
    request_kwargs.update(
        {
            "model": model,
            "messages": message_history,
            # "response_format": (
            #     {"type": "json_object"} if response_format == "json" else {}
            # ),
        }
    )
    try:
        response = client_together.chat.completions.create(**request_kwargs)
        completion = response.choices[0].message.content
        if response_format == "json":
            json_string_response = extract_json_part_from_string(completion)
            # #logger.info(
            #     "json_string_response Together model json: %s", json_string_response
            # )
            return json_string_response
        return completion
    except Exception as e:
        logger.error("Error using Togehter model %s: %s", model, e)
        if hasattr(e, "response") and e.response.headers:
            logger.error("Error Togehter rate limit info: %s ", e.response.headers)
            return None, e.response.headers
        return None


def extract_json_part_from_string(string):
    """Extract JSON from a string."""
    try:
        match = re.search(r"{.*}", string, re.DOTALL)
        if match:
            json_str = match.group(0)
            # return json.loads(json_str)
            return json_str
        else:
            logger.error("No valid JSON object found in the response content.")
            return None
    except json.JSONDecodeError as json_err:
        logger.error("JSON decode error: %s", json_err)
        return None


class RateLimitError(Exception):
    """Exception raised for rate limit errors."""

    def __init__(self, message="Rate limit exceeded", headers=None):
        super().__init__(message)
        self.headers = headers
