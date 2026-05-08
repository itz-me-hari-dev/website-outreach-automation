from dotenv import load_dotenv

from utils.logger import setup_logger

from search.search_service import (
    search_websites
)

from scraper.scraper_service import (
    scrape_multiple_websites
)

from summarizer.summarizer_service import (
    summarize_website_content
)

from email_generator.email_generator_service import (
    generate_email
)

from email_sender.mailgun_service import (
    EmailSenderService
)


load_dotenv()

logger = setup_logger()


def main():
    """
    Purpose:
    Main application entry point.

    Returns:
    None
    """

    logger.info(
        "Application started"
    )

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

    if not websites:

        logger.warning(
            "No websites found"
        )

        return

    print("\nFiltered Websites:\n")

    for website in websites:

        print(website)

    scraped_data = (
        scrape_multiple_websites(
            websites
        )
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

    print("\n")
    print("=" * 60)

    print(
        "COMPANY SUMMARIES"
    )

    print("=" * 60)

    for index, item in enumerate(
        summaries,
        start=1
    ):

        print("\n")
        print("=" * 60)

        print(
            f"{index}. "
            f"{item['url']}"
        )

        print("\nSummary:\n")

        print(
            item["summary"]
        )

    print("\n")
    print("=" * 60)

    total_companies = len(
        summaries
    )

    if total_companies == 1:

        choice_prompt = (
            "\nSelect company "
            "(1): "
        )

    else:

        available_options = ",".join(

            str(i)

            for i in range(
                1,
                total_companies + 1
            )
        )

        choice_prompt = (

            f"\nSelect company "
            f"({available_options} "
            f"or all): "

        )

    choice = input(
        choice_prompt
    ).strip().lower()

    if (
        choice == "all"
        and total_companies > 1
    ):

        selected_companies = (
            summaries
        )

    else:

        try:

            selected_indexes = [

                int(
                    x.strip()
                ) - 1

                for x in choice.split(
                    ","
                )

            ]

            selected_companies = [

                summaries[i]

                for i in (
                    selected_indexes
                )

            ]

        except (
            ValueError,
            IndexError
        ):

            logger.error(
                "Invalid selection"
            )

            return

    email_sender = (
        EmailSenderService()
    )

    for item in selected_companies:

        print("\n")
        print("=" * 60)

        print(
            f"Generating email for:"
            f" {item['url']}"
        )

        generated_email = (
            generate_email(
                item
            )
        )

        print(
            "\nGenerated Email:\n"
        )

        print(
            generated_email
        )

        response = (
            email_sender.send_email(
                subject=(
                    "Partnership "
                    "Opportunity"
                ),
                body=(
                    generated_email
                )
            )
        )

        if (
            response.status_code
            == 200
        ):

            logger.info(
                f"Email sent for "
                f"{item['url']}"
            )

            print(
                "\nEmail sent "
                "successfully"
            )

        else:

            logger.error(
                f"Failed to send "
                f"email for "
                f"{item['url']}"
            )

            print(
                "\nFailed to send "
                "email"
            )


if __name__ == "__main__":
    main()