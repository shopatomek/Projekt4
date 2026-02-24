import logging
import os
from logging.handlers import RotatingFileHandler

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 1. ŚCIEŻKI DO PLIKÓW
INTERNAL_LOG = os.path.join(LOG_DIR, "internal.log")  # Dla Analyzera (pełny)
APP_LOG = os.path.join(LOG_DIR, "app.log")  # Dla Ciebie (czysty)
CACHE_FILE = os.path.join(PROJECT_ROOT, "shared_data", "error_cache.json")


# 2. FILTR DLA APP.LOG
class SmartCleanFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage().lower()
        if record.levelno <= logging.INFO and "item" in msg:
            return False

        # Blokuj błędy w app.log TYLKO jeśli mamy już zapisany ich hash
        if record.levelno == logging.ERROR:
            if os.path.exists(CACHE_FILE):
                return False
        return True


# 3. KONFIGURACJA
logger = logging.getLogger("Projekt4Logger")
logger.setLevel(logging.INFO)

# Handler 1: INTERNAL.LOG (zapisuje wszystko, zero filtrów)
internal_handler = RotatingFileHandler(INTERNAL_LOG, maxBytes=1 * 1024 * 1024, backupCount=2, encoding="utf-8")
internal_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(internal_handler)

# Handler 2: APP.LOG (używa filtra, żeby było ładnie)
app_handler = RotatingFileHandler(APP_LOG, maxBytes=1 * 1024 * 1024, backupCount=5, encoding="utf-8")
app_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
app_handler.addFilter(SmartCleanFilter())
logger.addHandler(app_handler)
