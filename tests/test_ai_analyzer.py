import os  # noqa:F401
import tempfile  # noqa:F401 # Nieużywane bezpośrednio, ale przydatne do testowania z tymczasowymi plikami
import pytest
from app.ai_analyzer import (
    read_log_file,
    extract_log_levels,
    extract_modules,
    extract_errors_with_tracebacks,
    group_and_deduplicate_errors,
    build_ai_payload,
)

# --- FIXTURES ---

SAMPLE_LOG = """\
2026-03-03 12:00:00,001 | INFO | NEW SESSION STARTED | Automatic Monitoring Cycle
2026-03-03 12:00:00,002 | INFO | ==================================================
2026-03-03 12:00:00,003 | INFO | Scraper: start scraping data
2026-03-03 12:00:00,004 | INFO | Scraper: item 1 -> {'name': 'Eva', 'age': '25'}
2026-03-03 12:00:00,005 | INFO | Parser: start parsing data
2026-03-03 12:00:00,006 | INFO | Parser: successfully parsed item 1 -> {'name': 'Eva', 'age': 25}
2026-03-03 12:00:00,007 | ERROR | Parser: error parsing item 2 -> {'name': 'Noah', 'age': 'abc'}
2026-03-03 12:00:00,008 | INFO | Validator: start validation
2026-03-03 12:00:00,009 | ERROR | Validator: invalid age for item 3 -> {'name': 'Mia', 'age': -5}
2026-03-03 12:00:00,010 | ERROR | Parser: error parsing item 2 -> {'name': 'Noah', 'age': 'abc'}
"""


@pytest.fixture
def sample_log_lines():
    """Zwraca listę linii z przykładowego logu (po znaczniku sesji)."""
    lines = SAMPLE_LOG.strip().splitlines(keepends=True)
    # Symulujemy read_log_file — zwracamy linie po NEW SESSION STARTED
    fresh = []
    for line in reversed(lines):
        if "NEW SESSION STARTED" in line:
            break
        fresh.append(line)
    return fresh[::-1]


# --- TESTY JEDNOSTKOWE ---


def test_extract_log_levels_counts_correctly(sample_log_lines):
    levels = extract_log_levels(sample_log_lines)
    assert isinstance(levels, dict)
    assert levels.get("INFO", 0) > 0
    assert levels.get("ERROR", 0) > 0


def test_extract_log_levels_no_debug_in_sample(sample_log_lines):
    levels = extract_log_levels(sample_log_lines)
    assert "DEBUG" not in levels


def test_extract_modules_detects_all_three(sample_log_lines):
    modules = extract_modules(sample_log_lines)
    assert "Scraper" in modules
    assert "Parser" in modules
    assert "Validator" in modules


def test_extract_modules_counts_are_positive(sample_log_lines):
    modules = extract_modules(sample_log_lines)
    for count in modules.values():
        assert count > 0


def test_extract_errors_with_tracebacks_returns_list(sample_log_lines):
    errors = extract_errors_with_tracebacks(sample_log_lines)
    assert isinstance(errors, list)


def test_extract_errors_finds_correct_count(sample_log_lines):
    errors = extract_errors_with_tracebacks(sample_log_lines)
    # W sample_log_lines są 3 linie ERROR
    assert len(errors) == 3


def test_extract_errors_structure(sample_log_lines):
    errors = extract_errors_with_tracebacks(sample_log_lines)
    for err in errors:
        assert "message" in err
        assert "traceback" in err
        assert isinstance(err["traceback"], list)


# --- TESTY GRUPOWANIA I DEDUPLIKACJI ---


def test_group_and_deduplicate_reduces_duplicates():
    mock_errors = [
        {"message": "2026-03-03 | ERROR | Connection Timeout", "traceback": ["line 1"]},
        {"message": "2026-03-03 | ERROR | Connection Timeout", "traceback": ["line 1"]},
        {"message": "2026-03-03 | ERROR | Other Error", "traceback": []},
    ]
    grouped = group_and_deduplicate_errors(mock_errors)
    assert len(grouped) == 2


def test_group_and_deduplicate_count_field():
    mock_errors = [
        {"message": "2026-03-03 | ERROR | Timeout", "traceback": []},
        {"message": "2026-03-03 | ERROR | Timeout", "traceback": []},
        {"message": "2026-03-03 | ERROR | Timeout", "traceback": []},
    ]
    grouped = group_and_deduplicate_errors(mock_errors)
    assert grouped[0]["count"] == 3


def test_group_and_deduplicate_empty_input():
    grouped = group_and_deduplicate_errors([])
    assert grouped == []


def test_group_and_deduplicate_preserves_traceback():
    mock_errors = [
        {"message": "2026-03-03 | ERROR | SomeError", "traceback": ["tb_line_1", "tb_line_2"]},
    ]
    grouped = group_and_deduplicate_errors(mock_errors)
    assert grouped[0]["sample_traceback"] == ["tb_line_1", "tb_line_2"]


# --- TESTY KONTRAKTU PAYLOAD ---


def test_build_ai_payload_returns_dict():
    result = build_ai_payload()
    assert isinstance(result, dict)


def test_build_ai_payload_top_level_keys():
    result = build_ai_payload()
    if result:  # może być pusty jeśli brak nowych błędów
        for key in ["core", "logs", "validation", "instructions"]:
            assert key in result


def test_build_ai_payload_core_has_health_score():
    result = build_ai_payload()
    if result:
        assert "health_score" in result["core"]
        assert "error_rate" in result["core"]
        assert "%" in result["core"]["health_score"]


def test_build_ai_payload_logs_structure():
    result = build_ai_payload()
    if result:
        logs = result["logs"]
        assert "log_levels" in logs
        assert "modules_activity" in logs
        assert "unique_errors" in logs
        assert "new_errors_found" in logs
        assert isinstance(logs["unique_errors"], list)


def test_build_ai_payload_validation_status_valid():
    result = build_ai_payload()
    if result:
        assert result["validation"]["status"] in ("ok", "warning", "error")


def test_read_log_file_returns_list():
    lines = read_log_file()
    assert isinstance(lines, list)
