from app.scraper import scrape_demo_data
from app.parser import parse_data
from app.validator import validate_data
from app.logger import logger


def run_pipeline():
    """Główna funkcja uruchamiająca cały proces."""
    logger.info("==================================================")
    logger.info("NEW SESSION STARTED | Tracking fresh data")
    logger.info("==================================================")
    logger.info("Application: Pipeline execution started")

    # 1. Scrape
    raw_data = scrape_demo_data()

    # 2. Parse
    parsed_data = parse_data(raw_data)

    # 3. Validate
    validated_data = validate_data(parsed_data)

    logger.info(f"Final validated data ({len(validated_data)} items): " f"{validated_data}")
    return validated_data


if __name__ == "__main__":
    run_pipeline()
