"""
This file contains the implementation of the Together model for generating responses.
    """

import os
import re
from json_repair import repair_json
import json
import json5
from together import Together
from ...config.logging import logger

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))


def parse_llm_json(content):
    """Parse JSON from LLM response with fallbacks"""
    if not content:
        return None

    # Clean up markdown code blocks if present
    if content.startswith("```json\n") and content.endswith("\n```"):
        content = content[8:-4]
    content = content.replace("```", "").strip()

    # Try standard JSON parsing first
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning(f"Standard JSON parsing failed: {str(e)}")
        logger.warning(f"Problem at position {e.pos}, line {e.lineno}, col {e.colno}")
        logger.warning(f"Snippet around error: {content[max(0, e.pos-50):min(len(content), e.pos+50)]}")

    # Try json5 parsing next
    try:
        return json5.loads(content)
    except Exception as e:
        logger.warning(f"JSON5 parsing failed: {str(e)}")
        if hasattr(e, 'pos'):
            logger.warning(f"Snippet around error: {content[max(0, e.pos-50):min(len(content), e.pos+50)]}")

    # Try json_repair as last resort
    try:
        fixed = repair_json(content)
        return json.loads(fixed)
    except Exception as e:
        logger.error(f"All JSON parsing attempts failed: {str(e)}")
        logger.error("Full problematic content:")
        logger.error(content)
        return None


def get_response(prompt, quality="fast"):
    """Get a response from the Together model."""
    json_prompt_instructions = """
        Make sure your JSON response is valid JSON that respects the following instructions:
        - Does not include double quotes within strings
        - Does not duplicate double brackets or curly braces that might break the JSON
        - Is formatted correctly
        - Don't add newlines \n in the JSON response this will break the JSON - make sure strings are on a single line
        - Only include one JSON object in your response
        - Don't add ``` or prefix with json``` or anything like that. Just reply with valid JSON.
        - Comply with JSON format rules at all times. Make sure the content inside the properties won't break the JSON format.
        """
    try:
        if quality == "fast":
            model = "togethercomputer/llama-2-7b-chat"
        else:
            model = "togethercomputer/llama-2-70b-chat"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"{prompt}\n\n{json_prompt_instructions}"}
            ],
            response_format={
                "type": "json_object",
            },
            max_tokens=4096,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["</s>", "Human:", "Assistant:"],
            stream=False,
        )

        # logger.info(f"response: {response}")
    except Exception as e:
        logger.error("Error using Together model: %s", e)
        return None

    if response is None:
        return None

    content = response.choices[0].message.content
    parsed = parse_llm_json(content)

    if parsed:
        return json.dumps(parsed)  # Return standardized JSON string
    return None
