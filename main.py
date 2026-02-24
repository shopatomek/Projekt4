import time
import os
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


def run_agent_cycle():
    """
    Jeden pełny cykl: Znakowanie sesji -> Praca -> Analiza -> Persystencja
    """
    print(f"\n{'='*40}")
    print(f"🕒 START CYKLU: {time.strftime('%H:%M:%S')}")
    print(f"{'='*40}")

    # KROK 1: Nowa sesja (Filtr w logger.py teraz na to patrzy!)
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
        # Ten błąd zawsze zobaczysz, bo jest krytyczny (nie pochodzi z parsera/validatora)
        logger.error(f"Niespodziewany błąd krytyczny: {e}")

    # KROK 3: Analiza (Deduplikacja odbywa się wewnątrz build_ai_payload)
    payload = build_ai_payload()

    # KROK 4: Budowanie promptu
    prompt = build_prompt(payload)

    # KROK 5: Zapis do raportu
    if prompt:
        os.makedirs(SHARED_DIR, exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(prompt)

        new_errors = payload.get("logs", {}).get("new_errors_found", 0)
        logger.info(f"🚀 WYKRYTO NOWE BŁĘDY ({new_errors}). Raport: {REPORT_FILE}")
        print("❗ Znaleziono nowe błędy. Prompt wygenerowany.")
    else:
        # Jeśli prompt jest pusty, to znaczy, że błędy są stare (ukryte przez filtr)
        # albo system jest faktycznie czysty.
        logger.info("✅ System czysty. Brak nowych błędów w bieżącym interwale.")
        print("✅ Brak nowych błędów do raportowania.")


if __name__ == "__main__":
    # Upewniamy się, że folder na dane istnieje od razu
    os.makedirs(SHARED_DIR, exist_ok=True)

    logger.info("🚀 Agent monitorujący uruchomiony w Dockerze...")

    try:
        while True:
            run_agent_cycle()

            # Skróciłem interwał do 60s zgodnie z Twoim testowaniem
            print("😴 Następne sprawdzenie za 5 minut")
            time.sleep(300)
    except KeyboardInterrupt:
        logger.info("👋 Agent zatrzymany przez użytkownika.")
        print("\nZatrzymano.")
