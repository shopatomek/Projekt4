import os
from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt


def test_build_prompt_output():
    # 1. Pobieramy dane (Payload)
    payload = build_ai_payload()

    # 2. Generujemy prompt
    prompt = build_prompt(payload)

    print("\n" + "🤖" * 15)
    print("DEBUG: AI ADAPTER TEST")
    print("🤖" * 15 + "\n")

    # 3. Logika weryfikacji zależna od danych
    if not prompt:
        # Scenariusz A: BRAK BŁĘDÓW
        print("✅ STATUS: System czysty. Adapter zwrócił pusty string (prawidłowo).")

        # Sprzątamy stary plik, żeby n8n nie wysłało go przez pomyłkę
        if os.path.exists("shared_data/to_analyze.txt"):
            os.remove("shared_data/to_analyze.txt")
            print("🧹 Usunięto stary plik z folderu shared_data.")
    else:
        # Scenariusz B: SĄ BŁĘDY
        print("🚨 STATUS: Wykryto błędy. Generuję prompt...")
        print("-" * 30)
        print(prompt)
        print("-" * 30)

        # Weryfikacja struktury (Tylko gdy prompt NIE jest pusty)
        assert "SYSTEM CONTEXT" in prompt
        assert "UNIQUE ERROR ANALYSIS" in prompt
        assert "INSTRUCTIONS" in prompt

        # Zapisujemy plik dla n8n (To co zrobi Docker)
        os.makedirs("shared_data", exist_ok=True)
        with open("shared_data/to_analyze.txt", "w", encoding="utf-8") as f:
            f.write(prompt)
        print("\n📂 Zapisano prompt w: shared_data/to_analyze.txt")

    print("\n✅ Test zakończony pomyślnie.")


if __name__ == "__main__":
    test_build_prompt_output()
