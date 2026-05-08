import os
import time
import threading

from anthropic import Anthropic
from concurrent.futures import (
    ThreadPoolExecutor
)

from utils.logger import setup_logger


logger = setup_logger()

MAX_RETRIES = 3

RETRY_DELAY = 2

MAX_WORKERS = 3

email_semaphore = threading.Semaphore(2)

email_results_lock = threading.Lock()


def generate_single_email(
    summary_data: dict
) -> dict:
    """
    Purpose:
    Generate personalized outreach email.

    Inputs:
    summary_data (dict)

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

    url = summary_data.get("url")

    summary = summary_data.get(
        "summary",
        ""
    )

    prompt = f"""
Generate a professional cold outreach email.

Context:
The target company has already been analyzed.

Company Analysis:
{summary}

Product Being Pitched:
Encentro.ai

About Encentro.ai:
A platform for hyper-personalized
AI-powered email marketing automation.

Requirements:
- Professional tone
- Consultative approach
- Mention a relevant business insight
- Explain how Encentro.ai can help
- Add a clear CTA
- Keep concise
- Avoid sounding spammy

Return:
Subject line + email body.
"""

    for attempt in range(MAX_RETRIES):

        try:

            with email_semaphore:

                logger.info(
                    f"Generating outreach email "
                    f"for: {url}"
                )

                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=700,
                    temperature=0.5,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                email_content = (
                    response.content[0].text
                )

                logger.info(
                    f"Email generated for: "
                    f"{url}"
                )

                return {
                    "url": url,
                    "email": email_content
                }

        except Exception as error:

            logger.warning(
                f"Retry {attempt + 1}/"
                f"{MAX_RETRIES} failed for "
                f"{url}: {str(error)}"
            )

            time.sleep(RETRY_DELAY)

    logger.error(
        f"All email generation retries "
        f"failed for: {url}"
    )

    return {
        "url": url,
        "email": ""
    }


def generate_multiple_emails(
    summaries: list
) -> list:
    """
    Purpose:
    Generate emails concurrently.

    Inputs:
    summaries (list)

    Returns:
    list
    """

    generated_emails = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        future_results = executor.map(
            generate_single_email,
            summaries
        )

        for result in future_results:

            with email_results_lock:

                generated_emails.append(
                    result
                )

    logger.info(
        f"Generated "
        f"{len(generated_emails)} emails"
    )

    return generated_emails