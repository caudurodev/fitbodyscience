# config.py
import logging
from dotenv import load_dotenv
import os

load_dotenv(".env")


class Settings:
    """Settings class to hold all environment variables."""

    logger = logging.getLogger(__name__)
    LOG_LEVEL = os.environ["LOG_LEVEL"]
    assert LOG_LEVEL, "LOG_LEVEL is not set in environment variables"
    level = logging.getLevelName(LOG_LEVEL)
    logger.setLevel(level)  # logging.basicConfig(level=logging.DEBUG)
    logging_level = logging.getLevelName(logger.getEffectiveLevel())
    logger.format = (
        "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    # #logger.info("logging level:  %s", logging_level)

    HASURA_ADMIN_SECRET = os.environ["ADM_CUSTOM"]
    GRAPHQL_URL = os.environ["GRAPHQL_URL"]
    STORAGE_URL = os.environ["STORAGE_URL"]
    CONNECTION_STRING = os.environ["CONNECTION_STRING"]
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    GROQ_API_KEY = os.environ["GROQ_API_KEY"]
    TOGETHER_API_KEY = os.environ["TOGETHER_API_KEY"]

    OXYLABS_PASS = os.environ["OXYLABS_PASS"]
    OXYLABS_USER = os.environ["OXYLABS_USER"]

    SERPER_API_KEY = os.environ["SERPER_API_KEY"]
    BRIGHT_DATA_API_KEY = os.environ["BRIGHT_DATA_API_KEY"]
    APIFY_API_KEY = os.environ["APIFY_API_KEY"]
    USE_SCRAPER_API_KEY = os.environ["USE_SCRAPER_API_KEY"]

    if (
        os.environ["VERIFY_SSL_LOCAL_DEV"] == "False"
        or os.environ["VERIFY_SSL_LOCAL_DEV"] is None
    ):
        VERIFY_SSL_LOCAL_DEV = False
    else:
        VERIFY_SSL_LOCAL_DEV = True

    assert (
        HASURA_ADMIN_SECRET
    ), "HASURA_ADMIN_SECRET is not set in environment variables"

    assert OXYLABS_PASS, "OXYLABS_PASS is not set in environment variables"
    assert OXYLABS_USER, "OXYLABS_USER is not set in environment variables"
    assert SERPER_API_KEY, "SERPER API KEY is not set in environment variables"
    assert (
        BRIGHT_DATA_API_KEY
    ), "BRIGHT DATA API KEY is not set in environment variables"
    assert APIFY_API_KEY, "APIFY API KEY is not set in environment variables"

    assert GRAPHQL_URL, "GRAPHQL_URL is not set in environment variables"
    assert STORAGE_URL, "STORAGE_URL is not set in environment variables"
    assert CONNECTION_STRING, "CONNECTION_STRING is not set in environment variables"
    assert OPENAI_API_KEY, "OPENAI_API_KEY is not set in environment variables"
    assert TOGETHER_API_KEY, "TOGETHER_API_KEY is not set in environment variables"
    assert GROQ_API_KEY, "GROQ_API_KEY is not set in environment variables"
    assert (
        USE_SCRAPER_API_KEY
    ), "USE_SCRAPER_API_KEY is not set in environment variables"
    assert (
        VERIFY_SSL_LOCAL_DEV is not None
    ), "VERIFY_SSL_LOCAL_DEV is not set in environment variables"


settings = Settings()
logger = settings.logger
