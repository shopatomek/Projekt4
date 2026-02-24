from app.logger import logger


def scrape_demo_data():
    """
    Funkcja demo do pobierania danych.
    Zwraca listę słowników z polami 'name' i 'age'.
    """
    data = [
        {"name": "Eva", "age": "20"},
        {"name": "Noah", "age": "40"},
        {"name": "Liam", "age": "-30"},
        {"name": "Olivia", "age": "25"},
        {"name": "Ava", "age": "abc"},  # Błędna wartość wieku
        {"name": "Ethan", "age": "-35"},
        {"name": "Sophia", "age": "acafafas"},
        {"name": "Mason", "age": "-45"},
        {"name": "Isabella", "age": "dadafaas"},
        {"name": "Logan", "age": "-50"},
        {"name": "Mia", "age": "-30"},
        {"name": "Luna", "age": "dafsasxx"},
        {"name": "Lucas", "age": "-40"},
        {"name": "Amelia", "age": "das"},
        {"name": "Oliver", "age": "-25"},
        {"name": "Elijah", "age": "-35"},
        {"name": "Charlotte", "age": "afas"},
    ]

    logger.info("Scraper: start scraping data")
    for idx, item in enumerate(data, start=1):
        logger.info(f"Scraper: item {idx} -> {item}")
    logger.info(f"Scraper: finished, fetched {len(data)} items")
    return data
