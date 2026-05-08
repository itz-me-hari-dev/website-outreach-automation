from dotenv import load_dotenv

from utils.logger import setup_logger
from search.search_service import search_websites

from scraper.scraper_service import (
    scrape_multiple_websites
)

from summarizer.summarizer_service import (
    summarize_website_content
)

from email_generator.email_generator_service import (
    generate_multiple_emails
)


load_dotenv()

logger = setup_logger()


def main():
    """
    Purpose:
    Main application entry point.

    Returns:
    None

    Flowchart:
    outreach_flowchart.png

    Sequence Diagram:
    outreach_sequence_diagram.png

    Errors:
    None

    Side Effects:
    - Starts workflow
    """

    logger.info("Application started")

    keyword = input(
        "Enter search keyword: "
    ).strip()

    if not keyword:

        logger.error(
            "Keyword cannot be empty"
        )

        return

    websites = search_websites(
        keyword
    )

    print("\nFiltered Websites:\n")

    for website in websites:
        print(website)

    scraped_data = scrape_multiple_websites(
        websites
    )

    for item in scraped_data:

        print("\n")
        print("=" * 50)

        print(
            f"Website: {item['url']}"
        )

        print("\nContent Preview:\n")

        print(
            item["content"][:1000]
        )

    summaries = []

    for item in scraped_data:

        summary_result = (
            summarize_website_content(
                item
            )
        )

        summaries.append(
            summary_result
        )

    for item in summaries:

        print("\n")
        print("=" * 50)

        print(
            f"AI Summary for: "
            f"{item['url']}"
        )

        print("\n")

        print(item["summary"])

    generated_emails = (
        generate_multiple_emails(
            summaries
        )
    )

    for item in generated_emails:

        print("\n")
        print("=" * 50)

        print(
            f"Generated Email for: "
            f"{item['url']}"
        )

        print("\n")

        print(item["email"])


if __name__ == "__main__":
    main()