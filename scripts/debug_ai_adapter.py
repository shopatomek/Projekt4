from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt


def test_build_prompt_returns_string():
    # 1. Pobieramy dane (Payload)
    payload = build_ai_payload()
    
    # 2. Generujemy prompt na podstawie danych
    prompt = build_prompt(payload)
    
    # 3. Wyświetlamy wynik w konsoli (to co chciałeś zobaczyć)
    print("\n" + "="*30)
    print("DEBUG: GENERATED PROMPT")
    print("="*30 + "\n")
    
    print(prompt)
    
    print("\n" + "="*30)
    print("END OF PROMPT")
    print("="*30 + "\n")

    # 4. Weryfikacja (Logika testowa)
    # Jeśli któryś z tych assertów zawiedzie, skrypt wyrzuci błąd.
    # Jeśli jest cisza - znaczy, że wszystko jest zgodne z kontraktem.
    assert isinstance(prompt, str), "Prompt powinien być ciągiem znaków (str)"
    assert "SYSTEM CONTEXT" in prompt, "Brak sekcji SYSTEM CONTEXT w prompcie"
    assert "ERROR SUMMARY" in prompt, "Brak sekcji ERROR SUMMARY w prompcie"
    assert "INSTRUCTIONS" in prompt, "Brak sekcji INSTRUCTIONS w prompcie"
    
    print("✅ Wszystkie asercje zaliczone: Prompt jest poprawny technicznie.")


# KLUCZOWY ELEMENT: To uruchamia Twoją funkcję powyżej
if __name__ == "__main__":
    test_build_prompt_returns_string()