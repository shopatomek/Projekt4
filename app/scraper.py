from app.logger import logger


def scrape_demo_data():
    logger.info("Starting data scraping")
    data = [
        {"name": "Alice", "age": "25"},
        {"name": "Bob", "age": "thirty"},  # celowo błędne dane
        {"name": "Charlie", "age": "30"}
    ]
    logger.info(f"Scraper finished, got {len(data)} items")
    return data