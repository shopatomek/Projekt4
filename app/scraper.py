from app.logger import logger


def scrape_demo_data():
    """
    Funkcja demo do pobierania danych.
    Zwraca listę słowników z polami 'name' i 'age'.
    """
    data = [
        {"name": "Eva", "age": "20"},
        {"name": "Frank", "age": "35"},
        {"name": "Grace", "age": "-2"},  # błędne w walidatorze
        {"name": "Alice", "age": "25"},
        {"name": "Bob", "age": "thirty"},
        {"name": "Charlie", "age": "40"},
        {"name": "David", "age": "0"},
        {"name": "Eve", "age": "twenty"},
        {"name": "Frank", "age": "35"},
        {"name": "Grace", "age": "-22"},  # błędne w walidatorze
        {"name": "Bobby", "age": "-32"},
        {"name": "Cindy", "age": "seventy"},
        {"name": "Hank", "age": "zero"},
        {"name": "Eve", "age": "twenty"},
        {"name": "David", "age": "hundred"},
        {"name": "Zubu", "age": "-2"},
        {"name": "Yara", "age": "thirty"},
        {"name": "Xander", "age": "-40"},
        {"name": "Yara", "age": "thirty"},
    ]

    logger.info("Scraper: start scraping data")
    for idx, item in enumerate(data, start=1):
        logger.info(f"Scraper: item {idx} -> {item}")
    logger.info(f"Scraper: finished, fetched {len(data)} items")
    return data
