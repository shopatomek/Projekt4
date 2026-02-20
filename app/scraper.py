from app.logger import logger


def scrape_demo_data():
    """
    Funkcja demo do pobierania danych.
    Zwraca listę słowników z polami 'name' i 'age'.
    """
    data = [
        {"name": "Alice", "age": "25"},
        {"name": "Bob", "age": "thirty"},       # błędne
        {"name": "Charlie", "age": "30"},
        {"name": "Diana", "age": "-5"},         # błędne w walidatorze
        {"name": "Eve", "age": "22"},
    ]

    logger.info("Scraper: start scraping data")
    for idx, item in enumerate(data, start=1):
        logger.info(f"Scraper: item {idx} -> {item}")
    logger.info(f"Scraper: finished, fetched {len(data)} items")
    return data
