import logging
from datetime import datetime


LOG_FILE = "app.log"


def setup_logger():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def run_app():
    logging.info("Application started")

    # Celowo generujemy błąd
    try:
        result = 10 / 0
    except Exception as e:
        logging.error(f"Unhandled exception occurred: {e}")


if __name__ == "__main__":
    setup_logger()
    run_app()
