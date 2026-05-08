from dotenv import load_dotenv

from utils.logger import setup_logger
from search.search_service import search_websites


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

    keyword = input("Enter search keyword: ").strip()
    websites = search_websites(keyword)

    print("\nFiltered Websites:\n")

    for website in websites:
        print(website)


if __name__ == "__main__":
    main()