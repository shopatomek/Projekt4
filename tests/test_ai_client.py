import pytest  # noqa: F401
from app.ai_client import AIClient


def test_ai_client_mock_return_type():
    """Sprawdza, czy klient w trybie mock zwraca tekst."""
    client = AIClient(use_mock=True)
    # Dajemy mu coś, co wymusi analizę błędów, a nie Status OK
    response = client.get_analysis("TOTAL ERRORS: 5")

    assert isinstance(response, str)
    assert len(response) > 50
    # Szukamy słowa "Analiza", bo teraz mamy "[Dynamic Mock] Analiza Błędów"
    assert "Analiza" in response


def test_ai_client_real_not_implemented():
    """Sprawdza, czy klient informuje o braku implementacji realnego API."""
    client = AIClient(use_mock=False)
    response = client.get_analysis("Test")

    # Używamy 'in', żeby nie musieć wpisywać całego długiego zdania co do joty
    assert "Real API not implemented yet" in response


def test_ai_client_integration_with_adapter():
    """
    Sprawdza czy client przyjmuje to, co wypluwa adapter.
    """
    from app.ai_adapter import build_prompt

    fake_payload = {
        "core": {"total_log_lines": 10, "generated_at": "2026-02-20T12:00:00"},
        "logs": {"unique_errors": [], "log_levels": {}, "modules_activity": {}},
        "validation": {"status": "ok", "error_count": 0},
        "instructions": "Test instructions",
    }

    prompt = build_prompt(fake_payload)
    client = AIClient(use_mock=True)
    response = client.get_analysis(prompt)

    assert response is not None
    assert isinstance(response, str)
