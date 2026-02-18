import os
from app.logger import logger, LOG_FILE


def test_app_creates_log_file():
    # sprawdzamy, że plik logów istnieje
    assert os.path.exists(LOG_FILE), "Plik logów powinien istnieć"


def test_log_contains_info_and_error():
    # dopisujemy wpisy testowe
    logger.info("Test INFO")
    logger.error("Test ERROR")

    # odczytujemy plik logów
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.read()

    assert "Test INFO" in logs
    assert "Test ERROR" in logs
