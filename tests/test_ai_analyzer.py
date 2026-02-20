from app.ai_analyzer import (
    read_log_file,
    extract_log_levels,
    extract_modules,
    extract_errors_with_tracebacks,
    build_ai_payload,
    group_and_deduplicate_errors  # Dodajemy nową funkcję do testów
)

# --- TESTY JEDNOSTKOWE ---


def test_read_log_file():
    lines = read_log_file()
    assert isinstance(lines, list)
    assert len(lines) > 0


def test_extract_log_levels():
    lines = read_log_file()
    levels = extract_log_levels(lines)
    assert "INFO" in levels
    assert "ERROR" in levels


def test_extract_modules():
    lines = read_log_file()
    modules = extract_modules(lines)
    # Sprawdzamy czy przynajmniej jeden z modułów istnieje w logach
    assert any(m in modules for m in ["Scraper", "Parser", "Validator"])


def test_extract_errors_with_tracebacks():
    lines = read_log_file()
    errors = extract_errors_with_tracebacks(lines)
    assert isinstance(errors, list)
    if len(errors) > 0:
        error = errors[0]
        assert "message" in error
        assert "traceback" in error

# --- NOWY TEST LOGIKI GRUPOWANIA ---


def test_group_and_deduplicate_errors():
    # Tworzymy sztuczne dane, żeby sprawdzić czy grupowanie działa
    mock_errors = [
        {"message": "2024-02-20 | ERROR | Connection Timeout", "traceback": ["line 1"]},
        {"message": "2024-02-20 | ERROR | Connection Timeout", "traceback": ["line 1"]},
        {"message": "2024-02-20 | ERROR | Other Error", "traceback": []}
    ]
    grouped = group_and_deduplicate_errors(mock_errors)
    
    # Powinniśmy mieć 2 unikalne błędy zamiast 3 surowych
    assert len(grouped) == 2
    # Sprawdzamy czy licznik (count) działa
    timeout_err = next(e for e in grouped if "Connection Timeout" in e["message"])
    assert timeout_err["count"] == 2

# --- ZAKTUALIZOWANY TEST KONTRAKTU DLA AI ---


def test_build_ai_payload_contract():
    payload = build_ai_payload()

    # Poziom 1 - główne sekcje
    assert isinstance(payload, dict)
    assert all(key in payload for key in ["core", "logs", "validation", "instructions"])

    # Poziom 2 - sekcja 'core'
    assert "total_log_lines" in payload["core"]
    assert "generated_at" in payload["core"]

    # Poziom 2 - sekcja 'logs' (TUTAJ NAJWIĘKSZE ZMIANY)
    logs = payload["logs"]
    assert isinstance(logs["log_levels"], dict)
    assert isinstance(logs["modules_activity"], dict)
    
    # Zmieniliśmy 'errors' na 'unique_errors'
    assert "unique_errors" in logs
    assert isinstance(logs["unique_errors"], list)
    assert "total_errors_detected" in logs

    # Sprawdzamy strukturę unikalnego błędu (jeśli jakieś są)
    if len(logs["unique_errors"]) > 0:
        first_unique = logs["unique_errors"][0]
        assert "message" in first_unique
        assert "count" in first_unique
        assert "sample_traceback" in first_unique

    # Poziom 2 - sekcja 'validation'
    validation = payload["validation"]
    assert validation["status"] in ("ok", "warning", "error")
    assert "error_count" in validation

    # Poziom 2 - sekcja 'instructions'
    assert isinstance(payload["instructions"], str)
    assert "unique_errors" in payload["instructions"] 