""" This module extracts assertions from long text and adds them to the content store """

import json
from ..vendors.llm.get_response import get_response
from ..utils.config import logger
from ..vendors.llm.get_response import count_tokens


def evaluate_transcript_for_science_based(text_content):
    """extract assertions from long text"""
    total_tokens = count_tokens(text_content)
    if total_tokens > 16000:
        logger.info("Text too long, truncating to 16000 tokens")
        text_content = f"{text_content[:16000]} note:(text has been truncated to first 16000 tokens)"
    try:
        evaluation = get_response(
            f"""
            Evaluate this text: 
            
            {text_content}

            your task is to evaluate and give a true or false evaluation if the text
            is talking about science and whether what is being said can be proven or disproven
            by scientific evidence. 

            Return valid JSON response like this:
            {{  
                "evaluation":"<true | false>",
                "reason":"The text is talking about science and can be proven or disproven by scientific evidence"
            }}
        """,
            quality="fast",
        )
        # #logger.info("Assertions found: %s", assertions)
        try:
            evaluation_json = json.loads(evaluation)
            return evaluation_json
        except Exception as e:
            logger.error("Error parsing evaluation: %s", e)
            logger.info("evaluation %s", evaluation)
            logger.info("evaluation_json %s", evaluation_json)
            return None
    except Exception as e:
        logger.error("Error evaluating assertions: %s", e)
        return None
