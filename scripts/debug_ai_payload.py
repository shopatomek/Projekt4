import json
from app.ai_analyzer import build_ai_payload
from app.logger import logger  # Importujemy loggera

# Funkcje przetwarzania
from app.scraper import scrape_demo_data
from app.parser import parse_data
from app.validator import validate_data

if __name__ == "__main__":
    print("🔄 Wymuszam uruchomienie systemu i znakowanie nowej sesji...")

    # KLUCZOWY MOMENT: Wbijamy flagę nowej sesji do pliku logów
    logger.info("==================================================")
    logger.info("NEW SESSION STARTED | Debugging Payload")
    logger.info("==================================================")

    # KROK 1: Generowanie logów do pliku app.log
    data = scrape_demo_data()
    parsed = parse_data(data)
    validate_data(parsed)

    print("✅ Logi zapisane (oznaczone jako nowa sesja). Rozpoczynam analizę...\n")

    # KROK 2: Analiza logów z pliku
    # Teraz build_ai_payload() zatrzyma się na powyższym znaczniku!
    payload = build_ai_payload()

    print("🚀" * 15)
    print("DEBUG: AI PAYLOAD JSON")
    print("🚀" * 15 + "\n")

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    # Weryfikacja liczników (używamy nowych nazw kluczy!)
    new_errors = payload["logs"].get("new_errors_found", 0)
    unique_types = len(payload["logs"].get("unique_errors", []))

    print("\n" + "=" * 30)
    print(f"New Raw Errors (This Session): {new_errors}")
    print(f"Unique Error Types: {unique_types}")
    print("=" * 30)
