import logging
import os
import json
from logging.handlers import RotatingFileHandler

# Ścieżka do cache - MUSI być taka sama jak w ai_analyzer.py
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "error_cache.json")


class SmartCleanFilter(logging.Filter):
    def _get_last_hash(self):
        """Sprawdza, czy mamy zapisany hash błędów z poprzedniej sesji."""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    return json.load(f).get("last_hash", "")
            except Exception:
                return ""
        return ""

    def filter(self, record):
        msg = record.getMessage().lower()

        # 1. Zawsze wycinaj INFO o itemach
        if record.levelno <= logging.INFO and "item" in msg:
            return False

        # 2. Jeśli to jest ERROR, sprawdź czy mamy jakikolwiek hash
        # Jeżeli hash istnieje (czyli błędy zostały już raz zaraportowane),
        # blokujemy wyświetlanie kolejnych ERRORów w app.log.
        if record.levelno == logging.ERROR:
            if self._get_last_hash():
                return False

        return True


# --- KONFIGURACJA LOGGERA (Twoja stała struktura) ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

handler = RotatingFileHandler(LOG_FILE, maxBytes=1 * 1024 * 1024, backupCount=5, encoding="utf-8")

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)

# PODPIĘCIE FILTRA
handler.addFilter(SmartCleanFilter())

logger = logging.getLogger("Projekt4Logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
