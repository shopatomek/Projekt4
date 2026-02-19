from app.ai_analyzer import (
    read_log_file,
    extract_log_levels,
    extract_modules,
    extract_errors_with_tracebacks,
    build_ai_payload,
)


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


def test_build_ai_payload():
    payload = build_ai_payload()

    assert "total_log_lines" in payload
    assert "log_levels" in payload
    assert "modules_activity" in payload
    assert "errors" in payload
    assert "error_summary" in payload
