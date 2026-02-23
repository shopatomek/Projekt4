from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt


def test_build_prompt_output():
    # 1. Pobieramy dane (Payload)
    payload = build_ai_payload()

    # 2. Generujemy prompt na podstawie danych
    prompt = build_prompt(payload)

    # 3. Wyświetlamy wynik w konsoli
    print("\n" + "🤖" * 15)
    print("DEBUG: GENERATED PROMPT FOR AI")
    print("🤖" * 15 + "\n")

    print(prompt)

    print("\n" + "=" * 30)
    print("END OF PROMPT")
    print("=" * 30 + "\n")

    # 4. Weryfikacja (Dostosowana do nowej logiki)
    assert isinstance(prompt, str), "Prompt powinien być ciągiem znaków (str)"
    assert "SYSTEM CONTEXT" in prompt, "Brak sekcji SYSTEM CONTEXT"
    assert (
        "UNIQUE ERROR ANALYSIS" in prompt
    ), "Brak sekcji UNIQUE ERROR \
        ANALYSIS"
    assert "INSTRUCTIONS" in prompt, "Brak sekcji INSTRUCTIONS"

    # Sprawdzamy czy widać grupowanie jeśli są błędy
    if payload["validation"]["error_count"] > 0:
        assert (
            "OCCURRENCES:" in prompt
        ), "Brak informacji o liczbie wystąpień \
            błędów"

    print("✅ Sukces: Prompt wygenerowany poprawnie zgodnie z nowym formatem.")


if __name__ == "__main__":
    test_build_prompt_output()
