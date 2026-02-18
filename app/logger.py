import logging
import os
from logging.handlers import RotatingFileHandler

# absolutna ścieżka do katalogu Projekt4
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# plik logów
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# konfiguracja RotatingFileHandler
handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1 * 1024 * 1024,  # 1 MB
    backupCount=5,             # maksymalnie 5 starych plików
    encoding="utf-8"
)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)

# główny logger
logger = logging.getLogger("Projekt4Logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# dodajemy opcjonalnie console output podczas developmentu
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# dodajemy opcjonalnie file output podczas developmentu
dev_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1 * 1024 * 1024,  # 1 MB
    backupCount=5,             # maksymalnie 5 starych plików
    encoding="utf-8"
)
dev_handler.setFormatter(formatter)
logger.addHandler(dev_handler)