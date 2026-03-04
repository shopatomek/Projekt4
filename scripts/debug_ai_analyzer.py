import os
import sys
from app.scraper import scrape_demo_data
from app.parser import parse_data
from app.validator import validate_data
from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt
from app.logger import logger, INTERNAL_LOG

# Upewniamy się że jesteśmy w katalogu projektu
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def run_debug():
    """
    Testuje pełny przepływ lokalnie bez Dockera:
    1. Generuje nową sesję (Scraper -> Parser -> Validator)
    2. Analizuje świeże logi (build_ai_payload)
    3. Buduje prompt (build_prompt)
    4. Wyświetla wynik
    """

    # KROK 1: Sprawdzenie środowiska
    print(f"\n{'='*50}")
    print("DEBUG: AI ANALYZER — FULL FLOW TEST")
    print(f"{'='*50}")

    if not os.path.exists(INTERNAL_LOG):
        print(f"⚠️  Plik logu nie istnieje: {INTERNAL_LOG}")
        print("   Zostanie utworzony automatycznie.\n")

    # KROK 2: Generowanie nowej sesji logów
    print("\n🚀 KROK 1: Uruchamiam potok danych (Scraper → Parser → Validator)...")
    logger.info("==================================================")
    logger.info("NEW SESSION STARTED | Debugging AI Analyzer")
    logger.info("==================================================")

    data = scrape_demo_data()
    parsed = parse_data(data)
    validate_data(parsed)
    print(f"   ✅ Wygenerowano {len(data)} rekordów.")

    # KROK 3: Analiza logów
    print("\n📊 KROK 2: Analizuję logi z bieżącej sesji...")
    payload = build_ai_payload()

    if not payload:
        print("   ℹ️  Brak nowych błędów (te same co w poprzednim cyklu lub brak błędów).")
        print("   💡 Usuń shared_data/error_cache.json aby wymusić analizę.")
        return

    error_count = payload["logs"]["new_errors_found"]
    unique_types = len(payload["logs"]["unique_errors"])
    health = payload["core"]["health_score"]
    error_rate = payload["core"]["error_rate"]

    print(f"   📌 Błędy surowe:    {error_count}")
    print(f"   📌 Typy unikalne:   {unique_types}")
    print(f"   📌 Health Score:    {health}")
    print(f"   📌 Error Rate:      {error_rate}")

    # KROK 4: Generowanie promptu
    print("\n📝 KROK 3: Generuję prompt dla AI...")
    prompt = build_prompt(payload)

    print(f"\n{'🤖'*15}")
    print("WYGENEROWANY PROMPT:")
    print(f"{'🤖'*15}\n")
    print(prompt)
    print(f"\n{'='*50}")

    # KROK 5: Weryfikacja
    assert isinstance(prompt, str), "❌ Prompt musi być stringiem!"
    assert "SYSTEM CONTEXT" in prompt, "❌ Brak sekcji SYSTEM CONTEXT"
    assert "UNIQUE ERROR ANALYSIS" in prompt, "❌ Brak sekcji UNIQUE ERROR ANALYSIS"
    assert "INSTRUCTIONS" in prompt, "❌ Brak sekcji INSTRUCTIONS"

    print("✅ Weryfikacja struktury: OK")
    print(f"✅ Długość promptu: {len(prompt)} znaków")
    print("\n✅ Debug zakończony pomyślnie.")


if __name__ == "__main__":
    try:
        run_debug()
    except Exception as e:
        print(f"\n❌ BŁĄD: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
