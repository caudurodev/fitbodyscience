""" This module extracts assertions from long text and adds them to the content store """

import json
from ..utils.llm import get_llm_completion
from ..utils.config import logger


def extract_assertions_from_long_text(
    long_text, additional_information, related_content
):
    """extract assertions from long text"""
    try:
        assertions = get_llm_completion(
            f"""
            Given this long text: 
            
            {long_text}

            and additional infortmation about the long text (possibly links to evidence, etc.):

            {additional_information}

            here are saved links related to the text in json format:

            {related_content}

            Return a JSON with all of the assertions mentioned in thge long text and categorize them 
            as assertions that are based on scientific evidence, or likely false assertions such as
            assertions that are based on misinformation, conspiracy theories, or fake news.
            
            in the "assertion_type" json property: add the most likely type of assertion such as true or false.
            in the "evidence_type" json property: add the evidence that supports the assertion if the video 
            mentions the evidence. 
           
            in the "fallacy" json property: add the type of fallacy if the assertion is likely false.

            in the "main_point" json property: add one or more main point of the texts. What are the main assertions?
            
            in the "tags" json property: add the tags that describe the text.

            "part_of_text_assertion_made" json property: add the sentence where the assertion was made from original text.
            
            "part_of_transcript_assertion_timestamp" json property: add the timestamp of the assertion in the video transcript if timestamp is present.
            
            "assertion_weight" is a json property that tries to rank how important the individual assertion is to the main point
            of the long text - it should be a value of 0 to 10 in which 0 is irrelevant and 10 is so critical, the main point is
            not made without it.

            "assertion_search_verify" Create a text that will be used to verify the assertion in a search engine. It should be a complete
            sentence that is precise in encapsulating the assertion, specific subject matter and topics and should lead to evidence that verifies of falsifies the assertion.

            "standalone_assertion_reliability": is an evaluation of the assertion by itself without the larger context. 
            Does it make sense, is it factual, does it rely on good evidence to be made. A score of 0 to 10 where 0 is completely unreliable and 10 
            is completely reliable should be given.

            "why_relevant_main_point" is a short explanation of why the assertion is relevant to the main point of the text.
            "assertion_context" is a short explanation of the context of the assertion so that readers can understand what topics
            it is referring to. It should add clarity about the topics and subject matter.
            in the citation, add any relevant links provided in the text or additional text that are relevant to the assertion.
            Add the sources of the evidence if the text mentions the source. The source can be links, people, studies, etc. If the 
            citation is the same as the saved links related to the text, add the with the correct uuid in contentId.

            Don't add assertions not from the text. Don't add evidence that is not from the text.

            Ignore any promotional content in the text or sponsored content. If the sponsored content is clearly
            a conflict of interest, ignore it. Add any conflict of interest to the "conflict_of_interest" json property.conflit_of_interest

            In "main_conclusion" property add the main conclusion of the text for which most assertions are relevant for.
            In "why_relevant" property add a short explanation of why the evidence is relevant to the assertion.
            In "content_weight_to_assertion" property add a score of 0 to 10 where 0 is irrelevant and 10 is so critical to have the evidence to support the assertion.

            Make sure to extract all important assertions that make up the core of the argument.
            When returning JSON, make sure to return a valid JSON response, fixing things like unnecessary trailing commas.
            Return valid JSON response like this:
            {{  
                "main_conclusion":"The main point most of the assertions are trying to make",
                "assertions": [
                    {{
                        "assertion_weight":"3",
                        "standalone_assertion_reliability":"4",
                        "why_relevant_main_point":"",
                        "assertion":"The earth is round",
                        "assertion_context":"we are talking about the shape of the earth",
                        "assertion_search_verify":"",
                        "part_of_text_assertion_made": "",
                        "part_of_transcript_assertion_timestamp": "3:12",
                        "assertion_type": "true",
                        "fallacy": "none",
                        "evidence_type":"The earth is round because it has been observed from space",
                        "citations":[
                            {{
                                "url":"https://www.tandfonline.com/doi/full/10.1186/1550-2783-10-39",
                                "contentId":"uuid",
                                "why_relevant":"",
                                "content_weight_to_assertion":"3"
                            }}
                        ]
                    }}
                ]
            }}
        """
        )
        # #logger.info("Assertions found: %s", assertions)
        try:
            assertions_json = json.loads(assertions)
            return assertions_json
        except Exception as e:
            logger.error("Error parsing assertions: %s", e)
            logger.info("assertions %s", assertions)
            return None
    except Exception as e:
        logger.error("Error extracting assertions: %s", e)
        return None
