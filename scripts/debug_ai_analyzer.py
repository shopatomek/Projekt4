import os
from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt
from app.logger import LOG_FILE, logger
from main import run_pipeline  # Importujemy funkcję, która faktycznie odpala Scrapera


def test_build_prompt_output():
    """
    Testuje pełny przepływ:
    1. Uruchomienie nowej sesji (run_pipeline)
    2. Analiza świeżych logów (build_ai_payload)
    3. Generowanie promptu (build_prompt)
    """

    # KROK 1: Sprawdzenie środowiska
    if not os.path.exists(LOG_FILE):
        logger.warning(f"Plik logu {LOG_FILE} nie istnieje. Zostanie utworzony.")

    print("\n🚀 KROK 1: Uruchamiam potok danych (Scraper -> Parser -> Validator)...")
    # To wygeneruje wpis "NEW SESSION STARTED" i nowe błędy (Cindy, Bobby)
    run_pipeline()

    print("\n📊 KROK 2: Pobieram dane z ostatniej sesji logów...")
    payload = build_ai_payload()

    # Wyciągamy licznik, żeby sprawdzić czy Bobby i Cindy weszli
    error_count = payload["validation"]["error_count"]
    unique_types = len(payload["logs"]["unique_errors"])

    print(f"   INFO: Wykryto {error_count} błędów surowych.")
    print(f"   INFO: Zredukowano do {unique_types} unikalnych typów.")

    print("\n📝 KROK 3: Generuję prompt dla AI...")
    prompt = build_prompt(payload)

    # WYŚWIETLANIE WYNIKU
    print("\n" + "🤖" * 15)
    print("DEBUG: GENERATED PROMPT FOR AI")
    print("🤖" * 15 + "\n")
    print(prompt)
    print("\n" + "=" * 30)

    # KROK 4: Weryfikacja logiczna
    assert isinstance(prompt, str), "Prompt musi być tekstem!"
    assert "SYSTEM CONTEXT" in prompt, "Brak nagłówka System Context"

    if error_count >= 7:
        print(f"✅ SUKCES: Wykryto {error_count} błędów. Bobby i Cindy są w logach!")
    else:
        print(f"⚠️ UWAGA: Wykryto tylko {error_count} błędów. Sprawdź, czy zapisałeś scraper.py!")


if __name__ == "__main__":
    try:
        test_build_prompt_output()
    except Exception as e:
        logger.error(f"Debug script failed: {e}", exc_info=True)
