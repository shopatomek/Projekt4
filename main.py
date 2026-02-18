from app.scraper import scrape_demo_data
from app.parser import parse_data
from app.validator import validate_data
from app.logger import logger

if __name__ == "__main__":
    logger.info("Application started")

    # Scrape data
    raw_data = scrape_demo_data()

    # Parse data
    parsed_data = parse_data(raw_data)

    # Validate data
    validated_data = validate_data(parsed_data)

    logger.info(f"Final validated data: {validated_data}")









