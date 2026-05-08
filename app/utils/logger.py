import logging
import os


def setup_logger():
    """
    Purpose:
    Configure structured logging for the application.

    Returns:
    logging.Logger

    Flowchart:
    None

    Sequence Diagram:
    None

    Errors:
    None

    Side Effects:
    - Creates log file
    """

    os.makedirs("outputs/logs", exist_ok=True)

    logger = logging.getLogger("website_outreach")

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        "outputs/logs/application.log"
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger