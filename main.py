import time
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from app.logger import logger

# Importujemy metody Twojego systemu
from app.scraper import scrape_demo_data
from app.parser import parse_data
from app.validator import validate_data
from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt

# 1. SYNCHRONIZACJA ŚCIEŻEK
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHARED_DIR = os.path.join(BASE_DIR, "shared_data")
REPORT_FILE = os.path.join(SHARED_DIR, "to_analyze.txt")
LAST_REPORT_FILE = os.path.join(SHARED_DIR, "last_report.txt")

# 2. STREFA CZASOWA
TZ = ZoneInfo("Europe/Warsaw")


def now_local():
    return datetime.now(TZ).strftime("%H:%M:%S")


def run_agent_cycle():
    """
    Jeden pełny cykl: Znakowanie sesji -> Praca -> Analiza -> Persystencja
    """
    print(f"\n{'='*40}")
    print(f"🕒 START CYKLU: {now_local()}")
    print(f"{'='*40}")

    # KROK 1: Nowa sesja
    logger.info("==================================================")
    logger.info("NEW SESSION STARTED | Automatic Monitoring Cycle")
    logger.info("==================================================")

    # KROK 2: Praca modułów
    try:
        data = scrape_demo_data()
        parsed = parse_data(data)
        validate_data(parsed)
        print("✅ Praca modułów zakończona.")
    except Exception as e:
        logger.error(f"Niespodziewany błąd krytyczny: {e}")

    # KROK 3: Analiza
    payload = build_ai_payload()

    # KROK 4: Budowanie promptu
    prompt = build_prompt(payload)

    # KROK 5: Zapis do raportu
    if prompt:
        os.makedirs(SHARED_DIR, exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(prompt)

        new_errors = payload.get("logs", {}).get("new_errors_found", 0)
        # Logujemy ścieżkę last_report.txt (to co n8n zapisuje po analizie)
        logger.info(f"🚀 WYKRYTO NOWE BŁĘDY ({new_errors}). Raport: {LAST_REPORT_FILE}")
        print("❗ Znaleziono nowe błędy. Prompt wygenerowany.")
    else:
        logger.info("✅ System czysty. Brak nowych błędów w bieżącym interwale.")
        print("✅ Brak nowych błędów do raportowania.")


if __name__ == "__main__":
    os.makedirs(SHARED_DIR, exist_ok=True)

    logger.info("🚀 Agent monitorujący uruchomiony w Dockerze...")

    try:
        while True:
            run_agent_cycle()
            print("😴 Następne sprawdzenie za 5 minut")
            time.sleep(300)
    except KeyboardInterrupt:
        logger.info("👋 Agent zatrzymany przez użytkownika.")
        print("\nZatrzymano.")
