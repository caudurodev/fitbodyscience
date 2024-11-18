"""Email utilities"""

import requests
from ...config.constants import MAILGUN_API_KEY, MAILGUN_DOMAIN
from ...config.logging import logger


def send_mass_newsletter(recipient_list, subject, html, text):
    """Send a mass newsletter to a list of recipients"""
    try:
        response = requests.post(
            f"https://api.eu.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": "Curedigest <mailgun@mg.curedigest.com>",
                "to": recipient_list,
                "subject": subject,
                "text": text,
                "html": html,
                "o:tracking": "yes",  # Enable tracking
                "o:tracking-clicks": "htmlonly",  # Track clicks in HTML version
                "o:tracking-opens": "yes",  # Track email opens
            },
            timeout=30,
        )
        response.raise_for_status()
        logger.info(f"Email sent successfully. Status code: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending email: {str(e)}")
        if e.response is not None:
            logger.error(f"Response status code: {e.response.status_code}")
            logger.error(f"Response text: {e.response.text}")
        return e.response if e.response else None
