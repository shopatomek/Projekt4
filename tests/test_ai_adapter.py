from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt


def test_build_prompt_structure():
    """
    Testuje, czy adapter poprawnie generuje nowy format promptu
    oparty na unikalnych błędach.
    """
    payload = build_ai_payload()
    prompt = build_prompt(payload)

    # Podstawowe sprawdzenie typu
    assert isinstance(prompt, str)
    assert len(prompt) > 100  # Prompt nie powinien być pusty

    # Sprawdzenie obecności nowych sekcji (zgodnie z nowym ai_adapter.py)
    assert "SYSTEM CONTEXT" in prompt
    assert "MODULE ACTIVITY" in prompt
    assert "UNIQUE ERROR ANALYSIS" in prompt  # To zastąpiło ERROR SUMMARY
    assert "INSTRUCTIONS" in prompt

    # Sprawdzenie czy adapter poprawnie wyświetla dane o unikalnych błędach
    # Jeśli w logach są błędy, sprawdźmy czy pojawiają się kluczowe słowa
    if payload["validation"]["error_count"] > 0:
        assert "ERROR:" in prompt
        assert "OCCURRENCES:" in prompt
        assert "SAMPLE TRACEBACK:" in prompt


def test_build_prompt_empty_payload():
    """
    Sprawdza, jak adapter reaguje na brak danych.
    """
    prompt = build_prompt({})
    assert prompt == "No data available for analysis."