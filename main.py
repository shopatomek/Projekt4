import time
import os
from app.logger import logger
from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt

# Importujemy metody Twojego systemu
from app.scraper import scrape_demo_data
from app.parser import parse_data
from app.validator import validate_data


def run_agent_cycle():
    """
    Jeden pełny cykl: Znakowanie sesji -> Praca -> Analiza -> Persystencja
    """
    print(f"\n{'='*40}")
    print(f"🕒 START CYKLU: {time.strftime('%H:%M:%S')}")
    print(f"{'='*40}")

    # KROK 1: Wymuszenie nowej sesji w logach (Kluczowe dla ai_analyzer)
    logger.info("==================================================")
    logger.info("NEW SESSION STARTED | Automatic Monitoring Cycle")
    logger.info("==================================================")

    # KROK 2: Generowanie pracy (Scraper -> Parser -> Validator)
    # Tutaj pojawią się błędy w app.log, o ile scraper/validator je rzuci
    try:
        data = scrape_demo_data()
        parsed = parse_data(data)
        validate_data(parsed)
        print("✅ Praca modułów zakończona. Logi zapisane.")
    except Exception as e:
        logger.error(f"Niespodziewany błąd podczas pracy modułów: {e}")

    # KROK 3: Analiza tylko TEJ konkretnej sesji
    # ai_analyzer przeszuka logi od ostatniego "NEW SESSION STARTED"
    payload = build_ai_payload()

    # KROK 4: Budowanie promptu przez Adapter
    prompt = build_prompt(payload)

    # KROK 5: Zapis do shared_data, jeśli są błędy
    if prompt:
        os.makedirs("shared_data", exist_ok=True)
        file_path = "shared_data/to_analyze.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(prompt)

        new_errors = payload["logs"].get("new_errors_found", 0)
        logger.info(f"🚀 WYKRYTO BŁĘDY ({new_errors}). Raport zapisany w {file_path}")
        print(f"❗ Znaleziono błędy. Prompt gotowy do analizy.")
    else:
        logger.info("✅ System czysty. Brak nowych błędów w bieżącym interwale.")
        print("✅ Brak błędów do raportowania.")


if __name__ == "__main__":
    logger.info("🚀 Agent monitorujący uruchomiony (interwał: 5 minut)...")

    try:
        while True:
            run_agent_cycle()

            print("\n😴 Cykl zakończony. Następne sprawdzenie za 1 minut...")
            # 300 sekund = 5 minut
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("👋 Agent zatrzymany przez użytkownika.")
        print("\nPraca agenta zakończona.")
