"""Summarize text using llm"""

import json
from ..utils.llm import get_llm_completion
from ..utils.config import logger
from ..content_store.summary_store import add_summary_to_content


def conclusion_content_tree(content_id):
    """extract assertions from long text"""
    try:

        result = create_conclusion(
            long_text, summary, main_assertion, assertions_with_evidence
        )
        summary = result.get("summary", "")
        conclusion = result.get("conclusion", "")
        if summary:
            add_summary_to_content(
                content_id=video_content_id, summary=summary, conclusion=conclusion
            )
            return summary
        else:
            logger.error("Error summarising text")
            return None

    except Exception as e:
        logger.error("Error summarising text: %s", e)
        return None


def create_conclusion(long_text, summary, main_assertion, assertions_with_evidence):
    """summarise text"""
    try:
        conclusion = get_llm_completion(
            f"""
            An author stated:
            
            {long_text}

            From this, a summary was created:
            {summary}

            And from both, the main point of what the author was trying to say was summarised as:
            {main_assertion}

            Also the main assertions from what the author stated were researched and broken down into parts. Each
            assertion was weighed for imporatance to the main argument and evidence provided by the author was
            classified according to evidence based science criteria. Opposing evidence was also researched
            to see if there was evidence to disprove each assertion. Here is a summary of what was found:
            {assertions_with_evidence}

            Your task is to now give an evaluation of the author's argument now that we have analysed
            what was said, broken it down into parts, looked up the factual scientific evidence that backs or disproves
            the arguments made. Is it a trustworthy argument? Does it have flaws? Did the author distort the facts?
            Did the autho exagerate the facts? Did the author leave out important facts? Did the author use logical fallacies?

            
            Return valid JSON response like this:
            {{  
                "main_conclusion":"add the conclusion here about the author's argument", 
                "trustworthiness":"add the trustworthiness of the author's argument here",
                "fallacies":[{{
                    "where_in_text_fallacy_appears":"",
                    "fallacy":"",
                    "explanation":""
                }}],
                "distortions":[{{
                    "where_in_text_distortion_appears":"",
                    "distortion":"",
                    "explanation":""
                }}],
                "exagerations":[{{
                    "where_in_text_exageration_appears":"",
                    "exageration":"",
                    "explanation":""
                }}],
                "omissions":[{{
                    "where_in_text_omission_appears":"",
                    "omission":"",
                    "explanation":""
                }}],

            }}
        """
        )
        try:
            conclusion = json.loads(conclusion)

            return summary
        except Exception as e:
            logger.error("Error parsing summary: %s", e)
            return None
    except Exception as e:
        logger.error("Error extracting summary: %s", e)
        return None
