import os
import time

from anthropic import Anthropic

from utils.logger import setup_logger


logger = setup_logger()

MAX_CONTENT_LENGTH = 12000

MAX_RETRIES = 3

RETRY_DELAY = 2


def summarize_website_content(
    website_data: dict
) -> dict:
    """
    Purpose:
    Generate AI summary from website content.

    Inputs:
    website_data (dict)

    Returns:
    dict
    """

    api_key = os.getenv(
        "CLAUDE_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "CLAUDE_API_KEY is missing"
        )

    client = Anthropic(
        api_key=api_key
    )

    url = website_data.get("url")

    content = website_data.get(
        "content",
        ""
    )

    trimmed_content = content[
        :MAX_CONTENT_LENGTH
    ]

    prompt = f"""
Analyze the following website content.

Provide:
1. What the company does
2. Their target audience
3. Their key services
4. Possible marketing or outreach gaps

Website:
{url}

Content:
{trimmed_content}
"""

    for attempt in range(MAX_RETRIES):

        try:

            logger.info(
                f"Generating AI summary "
                f"for: {url}"
            )

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            summary = (
                response.content[0].text
            )

            logger.info(
                f"Summary generated for: "
                f"{url}"
            )

            return {
                "url": url,
                "summary": summary
            }

        except Exception as error:

            logger.warning(
                f"Retry {attempt + 1}/"
                f"{MAX_RETRIES} failed for "
                f"{url}: {str(error)}"
            )

            time.sleep(RETRY_DELAY)

    logger.error(
        f"All Claude retries failed "
        f"for: {url}"
    )

    return {
        "url": url,
        "summary": ""
    }