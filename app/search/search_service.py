import os
import requests

from utils.logger import setup_logger


logger = setup_logger()


def search_websites(keyword: str, limit: int = 5) -> list:
    """
    Purpose:
    Search Google results using Serper.dev API
    and return filtered website URLs.

    Inputs:
    keyword (str):
        Search keyword

    limit (int):
        Number of websites to return

    Returns:
    list:
        List of filtered URLs

    Flowchart:
    outreach_flowchart.png

    Sequence Diagram:
    outreach_sequence_diagram.png

    Errors:
    - ValueError:
        Missing API key
    - requests.RequestException:
        API/network failures

    Side Effects:
    - Makes external API request
    - Writes logs
    """

    api_key = os.getenv("SERPER_API_KEY")

    if not api_key:
        raise ValueError("SERPER_API_KEY is missing")

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "q": keyword,
        "num": limit
    }

    try:
        logger.info(f"Searching keyword: {keyword}")

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        organic_results = data.get("organic", [])

        filtered_urls = []

        blocked_domains = [
            "linkedin.com",
            "facebook.com",
            "instagram.com",
            "youtube.com",
            "twitter.com"
        ]

        for result in organic_results:

            link = result.get("link")

            if not link:
                continue

            if any(domain in link for domain in blocked_domains):
                continue

            filtered_urls.append(link)

        logger.info(
            f"Found {len(filtered_urls)} filtered URLs"
        )

        return filtered_urls

    except requests.RequestException as error:

        logger.error(
            f"Serper API request failed: {str(error)}"
        )

        return []