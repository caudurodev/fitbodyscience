""" This module extracts assertions from long text and adds them to the content store """

import json
from ..vendors.llm.get_response import get_response
from ..utils.config import logger
from ..vendors.llm.get_response import count_tokens


def evaluate_content_assertion_relevance(text_content, assertion):
    """extract assertions from long text"""
    total_tokens = count_tokens(text_content)
    if total_tokens > 32000:
        logger.info("Text too long, truncating to 4000 tokens")
        text_content = f"{text_content[:32000]} note:(text has been truncated to first 4000 tokens)"
    try:
        evaluation = get_response(
            f"""
            Your task the text below and see if it specifically related to the assertion below:
            assertion: {assertion}
            
            This is the text:
            
            {text_content}

            your task is to evaluate and give a true or false evaluation if the text is directly 
            supporting or contradicting the assertion or not related

            If the text identifies the DOI number, add it in the JSON otherwise leave it blank
           

            Return valid JSON response like this:
            {{  
                "is_directly_related_to_assertion":"<true | false>",
                "is_scientific_factual_content":"<true | false>",
                "reason_why_related":"explain why the text is directly related to the assertion",
                "reason_is_scientific_factual_content":"explain why the text is scientific factual content",
                "is_pro_assertion":"<true | false>",
                "reason_why_pro_assertion":"explain why the text is directly supporting the assertion",
                "is_contradicting_assertion":"<true | false>",
                "reason_why_contradicting_assertion":"explain why the text is directly contradicting the assertion",
                "doi_number":"<doi number>",
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
