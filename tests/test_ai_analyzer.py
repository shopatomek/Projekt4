from app.ai_analyzer import (
    read_log_file,
    extract_log_levels,
    extract_modules,
    extract_errors_with_tracebacks,
    build_ai_payload, 
)

# --- STARE TESTY JEDNOSTKOWE (ZOSTAWIAMY, SĄ SUPER) ---


def test_read_log_file():
    lines = read_log_file()
    assert isinstance(lines, list)
    assert len(lines) > 0


def test_extract_log_levels():
    lines = read_log_file()
    levels = extract_log_levels(lines)
    assert "INFO" in levels
    assert "ERROR" in levels
    assert levels["ERROR"] >= 1


def test_extract_modules():
    lines = read_log_file()
    modules = extract_modules(lines)
    assert "Scraper" in modules
    assert "Parser" in modules
    assert "Validator" in modules


def test_extract_errors_with_tracebacks():
    lines = read_log_file()
    errors = extract_errors_with_tracebacks(lines)
    assert isinstance(errors, list)
    assert len(errors) >= 1
    
    error = errors[0]
    assert "message" in error
    assert "traceback" in error

# --- NOWY TEST KONTRAKTU DLA AI (PODMIENIONY) ---


def test_build_ai_payload_contract():
    payload = build_ai_payload()

    # Poziom 1 - główne sekcje słownika
    assert isinstance(payload, dict)
    assert "core" in payload
    assert "logs" in payload
    assert "validation" in payload
    assert "instructions" in payload

    # Poziom 2 - sekcja 'core'
    assert isinstance(payload["core"], dict)
    assert "total_log_lines" in payload["core"]
    assert "generated_at" in payload["core"]

    # Poziom 2 - sekcja 'logs'
    logs = payload["logs"]
    assert isinstance(logs["log_levels"], dict)
    assert isinstance(logs["modules_activity"], dict)
    assert isinstance(logs["errors"], list)

    # Poziom 2 - sekcja 'validation'
    validation = payload["validation"]
    assert validation["status"] in ("ok", "warning", "error")
    assert "error_count" in validation

    # Poziom 2 - sekcja 'instructions'
    assert isinstance(payload["instructions"], str)