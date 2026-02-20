from app.logger import logger


def scrape_demo_data():
    """
    Funkcja demo do pobierania danych.
    Zwraca listę słowników z polami 'name' i 'age'.
    """
    data = [
        {"name": "Eva", "age": "20"},
        {"name": "Frank", "age": "35"}, 
        {"name": "Grace", "age": "-2"},         # błędne w walidatorze
        {"name": "Alice", "age": "25"},
        {"name": "Bob", "age": "thirty"},       # błędne
    ]
      
    logger.info("Scraper: start scraping data")
    for idx, item in enumerate(data, start=1):
        logger.info(f"Scraper: item {idx} -> {item}")
    logger.info(f"Scraper: finished, fetched {len(data)} items")
    return data
