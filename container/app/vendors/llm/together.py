"""
This file contains the implementation of the Together model for generating responses.
    """

import os
import json
import re
import json5
from together import Together
from ...config.logging import logger

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))


def get_response(prompt, quality="fast"):
    """Get a response from the Together model."""
    json_prompt_instructions = """
        Make sure your JSON response is valid JSON that respects the following instructions:
        - Does not include double quotes within strings
        - Is formatted correctly
        - Don't add newlines \n in the JSON response this will break the JSON - make sure strings are on a single line
        - Only include one JSON object in your response
        - Don't add ``` or prefix with json``` or anything like that. Just reply with valid JSON.
        - Comply with JSON format rules at all times. Make sure the content inside the properties won't break the JSON format.
        """
    try:
        if quality == "fast":
            model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
        else:
            model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"{prompt}\n\n{json_prompt_instructions}"}
            ],
            response_format={
                "type": "json_object",
            },
            max_tokens=32768,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>", "<|eom_id|>"],
            stream=False,
        )

        # logger.info(f"response: {response}")
    except Exception as e:
        logger.error("Error using Together model: %s", e)
        return None

    if response is None:
        return None

    content = response.choices[0].message.content
    if content.startswith("```json\n") and content.endswith("\n```"):
        content = content[8:-4]
    content = content.replace("```", "")

    try:
        json.loads(content)
        logger.info(f"json is fine!")
        return content
    except json.JSONDecodeError:
        try:
            logger.info(f"broken json: {content}")
            fixed_json_object = json5.loads(content)
            logger.info(f"fixed json: {fixed_json_object}")
            fixed_json = json.dumps(fixed_json_object)
            return fixed_json
        except json.JSONDecodeError as e:
            logger.error(f"Failed to  fix JSON: {e}")

            return None