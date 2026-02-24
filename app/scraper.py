import random
import string
from app.logger import logger

# Baza imion do losowania
NAMES = ["Eva", "Noah", "Liam", "Olivia", "Ava", "Ethan", "Sophia", "Mason", "Isabella", "Logan", "Mia", "Luna", "Lucas", "Amelia", "Oliver", "Elijah", "Charlotte"]


def generate_random_string(length=5):
    """Generuje losowy ciąg znaków (np. do psucia wieku)."""
    return "".join(random.choices(string.ascii_letters, k=length))


def scrape_demo_data():
    """
    Funkcja pobierająca dane.
    Dynamicznie generuje od 10 do 20 rekordów z różnym stopniem 'uszkodzenia'.
    """
    logger.info("Scraper: start scraping data")

    num_items = random.randint(10, 20)
    data = []

    for idx in range(1, num_items + 1):
        name = random.choice(NAMES)

        # Losujemy scenariusz: 60% poprawne, 20% błąd parsera, 20% błąd validatora
        scenario = random.random()

        if scenario < 0.60:
            # 1. IDEALNE DANE - wiek 18-99
            age = str(random.randint(18, 99))
        elif scenario < 0.80:
            # 2. BŁĄD PARSERA - wiek to losowe litery
            age = generate_random_string(random.randint(3, 8))
        else:
            # 3. BŁĄD VALIDATORA - wiek to ujemna liczba
            age = str(random.randint(-50, -1))

        item = {"name": name, "age": age}
        logger.info(f"Scraper: item {idx} -> {item}")
        data.append(item)

    logger.info(f"Scraper: finished, fetched {len(data)} items")
    return data
