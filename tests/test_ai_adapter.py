import pytest  # noqa: F401
from app.ai_adapter import build_prompt


# --- TESTY JEDNOSTKOWE Z MOCK PAYLOAD ---


def _make_payload(error_count=2):
    """Helper: buduje minimalny poprawny payload do testów."""
    unique_errors = [{"message": f"Parser: error parsing item {i} -> {{'name': 'Test', 'age': 'bad'}}", "count": 1, "sample_traceback": []} for i in range(1, error_count + 1)]
    return {
        "core": {
            "total_log_lines_in_session": 50,
            "generated_at": "2026-03-03T12:00:00",
            "health_score": "88.0%",
            "error_rate": "12.0%",
        },
        "logs": {
            "log_levels": {"INFO": 40, "ERROR": error_count},
            "modules_activity": {"Scraper": 20, "Parser": 20, "Validator": 10},
            "unique_errors": unique_errors,
            "new_errors_found": error_count,
        },
        "validation": {
            "status": "warning" if error_count < 5 else "error",
            "error_count": error_count,
        },
        "instructions": "Przeanalizuj błędy, zwróć uwagę na Health Score i zaproponuj rozwiązanie.",
    }


def test_build_prompt_returns_string():
    """Prompt musi być stringiem."""
    prompt = build_prompt(_make_payload())
    assert isinstance(prompt, str)


def test_build_prompt_not_empty():
    """Prompt nie może być pusty gdy są błędy."""
    prompt = build_prompt(_make_payload())
    assert len(prompt) > 100


def test_build_prompt_contains_required_sections():
    """Sprawdza obecność wszystkich wymaganych sekcji."""
    prompt = build_prompt(_make_payload())
    assert "SYSTEM CONTEXT" in prompt
    assert "MODULE ACTIVITY" in prompt
    assert "UNIQUE ERROR ANALYSIS" in prompt
    assert "INSTRUCTIONS" in prompt


def test_build_prompt_contains_health_metrics():
    """Sprawdza czy metryki health/error rate są w prompcie."""
    prompt = build_prompt(_make_payload())
    assert "Health Score" in prompt
    assert "Error Rate" in prompt
    assert "88.0%" in prompt


def test_build_prompt_contains_error_details():
    """Sprawdza czy szczegóły błędów są widoczne w prompcie."""
    prompt = build_prompt(_make_payload(error_count=2))
    assert "ERROR:" in prompt
    assert "OCCURRENCES:" in prompt


def test_build_prompt_empty_payload_returns_empty_string():
    """Pusty payload -> pusty string (nie crash)."""
    result = build_prompt({})
    assert result == ""


def test_build_prompt_no_errors_returns_empty_string():
    """Payload bez błędów -> pusty string."""
    payload = _make_payload(error_count=0)
    payload["logs"]["unique_errors"] = []
    result = build_prompt(payload)
    assert result == ""


def test_build_prompt_module_activity_visible():
    """Moduły powinny być widoczne w sekcji MODULE ACTIVITY."""
    prompt = build_prompt(_make_payload())
    assert "Scraper" in prompt
    assert "Parser" in prompt
    assert "Validator" in prompt


def test_build_prompt_error_count_visible():
    """Liczba błędów powinna być widoczna w prompcie."""
    prompt = build_prompt(_make_payload(error_count=3))
    assert "3" in prompt
