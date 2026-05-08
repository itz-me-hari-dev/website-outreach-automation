import threading
import time
import requests

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

from utils.logger import setup_logger


logger = setup_logger()

REQUEST_TIMEOUT = 20

MAX_WORKERS = 5

MAX_RETRIES = 3

RETRY_DELAY = 2

scraping_semaphore = threading.Semaphore(3)

results_lock = threading.Lock()


def clean_text(text: str) -> str:
    """
    Purpose:
    Clean extracted website text.

    Returns:
    str
    """

    return " ".join(text.split())


def scrape_single_page(url: str) -> str:
    """
    Purpose:
    Scrape and clean a single webpage.

    Inputs:
    url (str)

    Returns:
    str
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for attempt in range(MAX_RETRIES):

        try:

            with scraping_semaphore:

                logger.info(
                    f"Scraping page: {url}"
                )

                response = requests.get(
                    url,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )

                response.raise_for_status()

                soup = BeautifulSoup(
                    response.text,
                    "lxml"
                )

                for tag in soup([
                    "script",
                    "style",
                    "nav",
                    "footer",
                    "header",
                    "noscript"
                ]):
                    tag.decompose()

                text = soup.get_text(
                    separator=" "
                )

                return clean_text(text)

        except requests.RequestException as error:

            logger.warning(
                f"Retry {attempt + 1}/"
                f"{MAX_RETRIES} failed for "
                f"{url}: {str(error)}"
            )

            time.sleep(RETRY_DELAY)

    logger.error(
        f"All retries failed for: {url}"
    )

    return ""


def discover_internal_links(
    base_url: str
) -> list:
    """
    Purpose:
    Discover useful internal pages.

    Inputs:
    base_url (str)

    Returns:
    list
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    internal_links = []

    target_keywords = [
        "about",
        "service",
        "solutions",
        "company"
    ]

    try:

        response = requests.get(
            base_url,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        for anchor in soup.find_all(
            "a",
            href=True
        ):

            href = anchor["href"].lower()

            if any(
                keyword in href
                for keyword in target_keywords
            ):

                full_url = urljoin(
                    base_url,
                    href
                )

                if full_url not in internal_links:
                    internal_links.append(full_url)

        return internal_links[:3]

    except requests.RequestException as error:

        logger.error(
            f"Internal link discovery failed: "
            f"{str(error)}"
        )

        return []


def scrape_website(url: str) -> dict:
    """
    Purpose:
    Scrape homepage and internal pages.

    Inputs:
    url (str)

    Returns:
    dict
    """

    logger.info(
        f"Starting website scrape: {url}"
    )

    combined_content = ""

    homepage_content = scrape_single_page(
        url
    )

    combined_content += homepage_content

    internal_links = discover_internal_links(
        url
    )

    for internal_url in internal_links:

        internal_content = scrape_single_page(
            internal_url
        )

        combined_content += internal_content

    return {
        "url": url,
        "content": combined_content[:15000]
    }


def scrape_multiple_websites(
    websites: list
) -> list:
    """
    Purpose:
    Concurrently scrape multiple websites.

    Inputs:
    websites (list)

    Returns:
    list
    """

    scraped_results = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        future_results = executor.map(
            scrape_website,
            websites
        )

        for result in future_results:

            with results_lock:

                scraped_results.append(result)

    logger.info(
        f"Completed scraping "
        f"{len(scraped_results)} websites"
    )

    return scraped_results