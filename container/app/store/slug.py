"""Add user content to the database"""

import re
import json
from urllib.parse import urlparse
from unidecode import unidecode
from typing import Optional
from datetime import datetime
from ..utils.graphql import make_graphql_call
from ..utils.config import logger


def generate_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from a title
    """
    # Convert to lowercase and normalize unicode characters
    slug = unidecode(title.lower())
    # Replace any non-alphanumeric characters with hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    # Remove leading/trailing hyphens
    slug = slug.strip("-")

    return slug


def generate_unique_slug(title: str, table_name: str = "content") -> str:
    """
    Generate a unique slug from a title for any content type
    """
    slug = generate_slug(title)
    return make_unique_slug(slug, table_name)


def make_unique_slug(slug: str, table_name: str) -> str:
    """
    Ensure slug is unique within the specified table

    Args:
        slug: The base slug to make unique
        table_name: Database table name to check for uniqueness
    """
    query = {
        "variables": {"slug": slug},
        "query": f"""
        query CheckSlugExists($slug: String!) {{
            {table_name}(where: {{slug: {{_eq: $slug}}}}) {{
                id
            }}
        }}
        """,
    }

    original_slug = slug
    counter = 1

    while True:
        try:
            result = make_graphql_call(
                query, user_id=None, user_role=None, is_admin=True
            )

            # Add validation for the result structure
            if not result or "data" not in result:
                logger.error("Invalid GraphQL response: %s", result)
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                return f"{original_slug}-{timestamp}"

            existing_content = result["data"][table_name]

            # If no content exists with this slug, we can use it
            if not existing_content:
                return slug

            # Otherwise, append counter and try again
            slug = f"{original_slug}-{counter}"
            query["variables"]["slug"] = slug
            counter += 1

        except Exception as e:
            logger.error("Error checking slug uniqueness: %s", e)
            # In case of error, append timestamp to ensure uniqueness
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            return f"{original_slug}-{timestamp}"
