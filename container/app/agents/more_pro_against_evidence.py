"""This module contains the agent to get opposing viewpoints on a given topic"""

import os
import json
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from ..utils.config import logger, settings
from ..content_store.assertion_store import get_assertion_content
from ..utils.llm import extract_json_part_from_string

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"
os.environ["SERPER_API_KEY"] = settings.SERPER_API_KEY


def get_opposing_viewpoints(assertion_id):
    """Get opposing viewpoints on a given topic"""

    assertion = get_assertion_content(assertion_id)
    if not assertion:
        logger.error(f"No assertion found for id: {assertion_id}")
        return None

    try:
        # Build main claim with fallbacks for missing fields
        main_claim_parts = []
        if assertion.get("text"):
            main_claim_parts.append(assertion["text"])
        if assertion.get("originalSentence"):
            main_claim_parts.append(
                f"The original assertion text was: {assertion['originalSentence']}"
            )
        main_claim = ". ".join(main_claim_parts) + "."

        # Get evidence type with fallback
        evidence_type = assertion.get("evidenceType", "No evidence type provided")

        # Build context with fallbacks for missing content fields
        context_parts = []
        content = assertion.get("content", {}) or {}
        if content.get("title"):
            context_parts.append(content["title"])
        if content.get("summary"):
            context_parts.append(content["summary"])
        if content.get("canonicalUrl"):
            context_parts.append(f"from the url {content['canonicalUrl']}")
        if content.get("doiNumber"):
            context_parts.append(f"with the DOI {content['doiNumber']}")
        context = (
            " - ".join(filter(None, context_parts)) or "No additional context available"
        )

        # Get assertion search verify with fallback
        assertion_search_verify = assertion.get("assertionSearchVerify", "")

        # Get contents assertions with fallback
        already_provided_evidence_for = json.dumps(
            assertion.get("contents_assertions", [])
        )

    except Exception as e:
        logger.error("Error getting assertion content: %s", e)
        logger.info("assertion: %s", assertion)
        return None

    main_assertion = f"""
        The assertion is summarised as: 
        
        {main_claim}

        Evidence type provided to back up the assertion:
        {evidence_type}

        This assertion was made in the following context:
        {context}

        This evidence has already been provided for this assertion:
        {already_provided_evidence_for}

        Here is an example search engine query to try and find evidence for the assertion:
        {assertion_search_verify}
        """

    # #logger.info("main_assertion %s", main_assertion)
    # return

    desired_evidence = """
        The task is to find evidence that is directly related to the assertion in the scientific literature.
        Search for scientific papers or widely accepted evidence that **directly and specifically** prove or disprove the assertion and provide a summary of their findings.
        Prefer primary research and highly ranked hierarchy of evidence over opinion, articles, and specialist opinions.
        Only return results which have a DOI number. 

        The studies should be for or against the assertion. The study should contribute to or disprove the 
        point/assertion being made.

        **Ensure that the evidence directly addresses the specific aspects and nuances of the assertion, including any qualifiers, quantities, conditions, or comparisons mentioned.**
        Do not include studies that only partially relate to the assertion or that address a broader or different topic.
        For example, if the assertion is about "eating high amounts of vegetables is not the best approach for longevity," focus on studies that specifically examine whether consuming high amounts of vegetables is or is not the best approach for longevity, possibly in comparison to other dietary strategies.

        Never return any results that match the already provided source_urls, studies, etc. 
        All papers must be new and not duplicates of what was already provided.
        Only return papers that are about the same subject matter. 
        Don't provide evidence that is from a different field of study that is unrelated.
        For example, don't provide a study about energy from electricity to support a claim about energy from food. 
        """

    search_tool = SerperDevTool()

    science_researcher = Agent(
        role="Senior Scientist",
        goal="Make sure the evidence provided is accurate, relevant, and directly addresses the specific assertion",
        backstory="""
        You are an experienced scientific research assistant who has read thousands of peer-reviewed papers. 
        You are known for your ability to find relevant science papers that support or contradict a given assertion or fact about a topic.
        You are very precise and able to classify studies by their hierarchy of evidence.
        You are meticulous in ensuring that the evidence you find **directly addresses the specific aspects and nuances of the assertion, including any qualifiers, quantities, conditions, or comparisons mentioned**.
        You avoid including evidence that only partially relates to the assertion or that addresses a broader or different topic.
        You are able to find the best evidence to support or contradict a given assertion.
        """,
        verbose=False,
        allow_delegation=False,
        tools=[search_tool],
    )

    science_reviewer = Agent(
        role="Scientist Reviewer",
        goal="Make sure the evidence provided is accurate and relevant",
        backstory="""
        You are an expert in logical and factual assertions. 
        You excel at reviewing scientific papers and ensuring the evidence provided is accurate and relevant.
        You pay close attention to the precise wording of the assertion and ensure that the evidence provided **directly addresses all aspects and nuances of the assertion, including any qualifiers, quantities, conditions, or comparisons**.
        You review the work of others to make sure they complete their tasks correctly. 
        You make sure evidence is classified correctly and that any assertions are supported or contradicted by the evidence provided directly.
        Your task is to guide scientists to find the best evidence to support or contradict a given assertion and complete tasks successfully.
        You are critical of the data you receive and make sure it is accurate and relevant. 
        You reject any evidence that does not specifically support or contradict the assertion as it is stated.
        """,
        verbose=False,
        allow_delegation=True,
        tools=[search_tool],
    )

    evidence = Task(
        description=f"""
            Your task is to find papers that prove and disprove this assertion in the scientific literature:

            {main_assertion}

            Identify scientific papers or widely accepted evidence that **directly and specifically** prove or disprove this assertion and provide a summary of their findings.

            **Ensure that the evidence you find addresses the specific aspects and nuances of the assertion, including any qualifiers, quantities, conditions, or comparisons mentioned.**
            Do not include studies that only partially relate to the assertion or that address a broader or different topic.

            For example, if the assertion is "Eating high amounts of vegetables is not the best approach for longevity," focus on studies that specifically examine whether consuming high amounts of vegetables is or is not the best approach for longevity, possibly in comparison to other dietary strategies.

            Don't allow any papers that are not from the same field of study or are not directly related to the assertion—for example, providing a study about energy from electricity to support a claim about energy from food. 

            Don't use the original source of the assertion as a potential paper reference.

            Try to return at least one paper that proves the assertion and one that disproves it.
            If you cannot find papers to disprove, return `found_disproven` as false.
            If you cannot find papers to support, return `found_support` as false.

            Return only JSON format and nothing else. Don't explain, don't add any extra information or text to the response which is not pure JSON.
            """,
        expected_output="""
        {
            "found_support": <true|false>,
            "found_disproven": <true|false>,
            "evidence_supports": [
                {      
                    "title": "Title of the paper",
                    "canonical_url": "url where to find the paper",
                    "doi_number": "DOI number",
                    "how_assertion_is_supported": "How the assertion is supported by this paper",
                    "proof_assertion_is_true": "How the paper proves the assertion is true, what evidence is provided.",
                    "evidence_type": "Meta analysis, clinical trial, observational study, etc."
                }
            ],
            "evidence_disprove": [
                {
                    "title": "Title of the paper",
                    "canonical_url": "url where to find the paper",
                    "doi_number": "DOI number",
                    "how_assertion_is_disproven": "How the assertion is disproven by this paper",
                    "proof_assertion_is_false": "How the paper proves the assertion is false, what evidence is provided.",
                    "evidence_type": "Meta analysis, clinical trial, observational study, etc."
                }
            ]
        }""",
        agent=science_researcher,
    )

    review_research = Task(
        description=f"""
        Your task is to review the papers found by scientists to ensure they are 
        accurate and relevant. Specifically, verify whether they prove or disprove this assertion:

        {main_assertion}

        **Ensure that the evidence directly addresses the specific aspects and nuances of the assertion, including any qualifiers, quantities, conditions, or comparisons mentioned.**
        Reject any papers that do not directly relate to the assertion or that only partially address it.

        If the research has flaws, instruct the scientist to find better papers if 
        you judge it likely they will find better papers. Don't let them waste time.
        Don't allow papers which don't have a DOI number or are not directly related to the assertion.

        {desired_evidence}

        If the research is correct, then return the results of pro and against papers in 
        JSON format and nothing else. Don't explain, 
        don't add any extra information or text to the response which is not pure JSON.
        Remove research found that is not correctly classified or that is missing information. 
        Remove research that is not a scientific paper.

        """,
        expected_output="""
        {
            "found_support": <true|false>,
            "found_disproven": <true|false>,
            "evidence_supports": [
                {      
                    "title": "Title of the paper",
                    "canonical_url": "url where to find the paper",
                    "doi_number": "DOI number",
                    "how_assertion_is_supported": "How the assertion is supported by this paper",
                    "proof_assertion_is_true": "How the paper proves the assertion is true, what evidence is provided.",
                    "evidence_type": "Meta analysis, clinical trial, observational study, etc."
                }
            ],
            "evidence_disprove": [
                {
                    "title": "Title of the paper",
                    "canonical_url": "url where to find the paper",
                    "doi_number": "DOI number",
                    "how_assertion_is_disproven": "How the assertion is disproven by this paper",
                    "proof_assertion_is_false": "How the paper proves the assertion is false, what evidence is provided.",
                    "evidence_type": "Meta analysis, clinical trial, observational study, etc."
                }
            ]
        }""",
        agent=science_researcher,
    )

    crew = Crew(
        agents=[science_researcher, science_reviewer],
        tasks=[evidence, review_research],
        output_format="json",
        output_json=True,
        verbose=0,
    )

    result = crew.kickoff()

    # logger.info("######################")
    # logger.info("agent crewai result %s", result)

    try:
        # Convert CrewOutput to string if needed
        if hasattr(result, "raw_output"):
            result_str = result.raw_output
        else:
            result_str = str(result)

        result_json_string = extract_json_part_from_string(result_str)
        return json.loads(result_json_string)
    except Exception as e:
        logger.error("Error converting result to json: %s", e)
        return None
