""" This module contains the functions to get the user from the database """

from datetime import datetime
from ..config.logging import logger
from ..utils.graphql import make_graphql_call


def upsert_influencer(
    name: str,
    profile_img: str,
    yt_channel_info_jsonb: dict,
    yt_description: str,
    yt_url: str,
    slug: str,
):
    """Upsert influencer data into the database"""
    date_now = datetime.now().strftime("%Y-%m-%d")

    # Convert empty string to None for UUID field
    profile_img = profile_img if profile_img else None

    query = {
        "variables": {
            "name": name,
            "profileImg": profile_img,  # Will be None if empty string
            "ytChannelInfoJsonb": yt_channel_info_jsonb,
            "ytDescription": yt_description,
            "ytLastUpdated": date_now,
            "ytUrl": yt_url,
            "slug": slug,
        },
        "query": """
            mutation UpsertInfluencersMutation(
                $name: String!, 
                $profileImg: uuid, 
                $ytChannelInfoJsonb: jsonb = "", 
                $ytDescription: String = "", 
                $ytLastUpdated: date = "", 
                $ytUrl: String!,
                $slug: String!
            ) {
                insert_influencers(objects: {
                    name: $name, 
                    profileImg: $profileImg, 
                    ytChannelInfoJsonb: $ytChannelInfoJsonb, 
                    ytDescription: $ytDescription, 
                    ytLastUpdated: $ytLastUpdated, 
                    ytUrl: $ytUrl,
                    slug: $slug
                }, on_conflict: {constraint: influencers_pkey, update_columns: [
                        name, 
                        profileImg, 
                        ytChannelInfoJsonb, 
                        ytDescription, 
                        ytLastUpdated, 
                        ytUrl,
                        slug
                    ]
                }) {
                    affected_rows
                    returning {
                        id
                    }
                }
            }
        """,
    }
    try:
        response = make_graphql_call(query)
        if response.get("errors"):
            logger.error("GraphQL Error: %s", response["errors"])
            return None
        return response["data"]["insert_influencers"]
    except Exception as e:
        logger.error(f"Error upserting influencer: {e}")
        logger.info(f"Response: {response}")
        return None


def get_influencer_by_url(url: str):
    """Get influencer by URL"""
    query = {
        "variables": {"url": url},
        "query": """
            query CheckInfluencerExistsQuery($url: String!) {
                influencers(where: {ytUrl: {_eq: $url}}) {
                    id
                }
            }
        """,
    }

    try:
        response = make_graphql_call(query)
        if response.get("errors"):
            logger.error("GraphQL Error: %s", response["errors"])
            return None
        return response["data"]["influencers"]
    except Exception as e:
        logger.error(f"Error getting influencer by URL: {e}")
        return None
