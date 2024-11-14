""" Constants for the app """

import os
from dotenv import load_dotenv

load_dotenv(".env")

FLASK_ENV = os.environ["FLASK_ENV"]
ROOT_URL = os.environ["ROOT_URL"]

OXYLABS_PASS = os.environ["OXYLABS_PASS"]
OXYLABS_USER = os.environ["OXYLABS_USER"]

HASURA_ADMIN_SECRET = os.environ["ADM_CUSTOM"]
GRAPHQL_URL = os.environ["GRAPHQL_URL"]
VERIFY_SSL_LOCAL_DEV = os.environ["VERIFY_SSL_LOCAL_DEV"]

TOGETHER_API_KEY = os.environ["TOGETHER_API_KEY"]
STORAGE_URL = os.environ["STORAGE_URL"]

MAILGUN_API_KEY = os.environ["MAILGUN_API_KEY"]
MAILGUN_DOMAIN = os.environ["MAILGUN_DOMAIN"]
SENDER_EMAIL = os.environ["SENDER_EMAIL"]


UNPAYWALL_API_URL = "https://api.unpaywall.org/v2/"
EMAIL = "rod@cauduro.dev"

CROSSREF_API_URL = "https://api.crossref.org/works/"
ORCID_API_URL = "https://pub.orcid.org/v3.0/"
