import os
import re
from datetime import datetime
from collections import Counter, defaultdict
from app.logger import LOG_FILE, logger


def read_log_file():
    """Wczytuje cały plik logów do pamięci."""
    if not os.path.exists(LOG_FILE):
        logger.error("AI Analyzer: log file does not exist")
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logger.info(f"AI Analyzer: loaded {len(lines)} log lines")
    return lines


def extract_log_levels(log_lines):
    """Zlicza poziomy logów (INFO, ERROR, WARNING itd.)."""
    levels = Counter()
    for line in log_lines:
        match = re.search(r"\|\s(INFO|ERROR|WARNING|DEBUG)\s\|", line)
        if match:
            levels[match.group(1)] += 1
    return dict(levels)


def extract_modules(log_lines):
    """Przypisuje logi do modułów (Scraper / Parser / Validator)."""
    modules = Counter()
    for line in log_lines:
        if "Scraper:" in line:
            modules["Scraper"] += 1
        elif "Parser:" in line:
            modules["Parser"] += 1
        elif "Validator:" in line:
            modules["Validator"] += 1
    return dict(modules)


def extract_errors_with_tracebacks(log_lines):
    """Wyciąga błędy wraz z tracebackami."""
    errors = []
    current_error = None

    for line in log_lines:
        if "| ERROR |" in line:
            current_error = {
                "message": line.strip(),
                "traceback": []
            }
            errors.append(current_error)
        elif current_error and line.startswith("Traceback"):
            current_error["traceback"].append(line.strip())
        elif current_error and current_error["traceback"]:
            current_error["traceback"].append(line.rstrip())
    return errors


def summarize_errors(errors):
    """Tworzy statystyki typów błędów."""
    summary = defaultdict(int)
    for err in errors:
        if "ValueError" in err["message"]:
            summary["ValueError"] += 1
        elif "invalid age" in err["message"]:
            summary["ValidationError"] += 1
        else:
            summary["OtherError"] += 1
    return dict(summary)


def build_ai_payload():
    """
    Główna funkcja: Zbiera dane i układa je w 'Kontrakt AI'.
    To tutaj łączymy Twoją logikę z nową strukturą.
    """
    # 1. Pobieramy surowe dane Twoimi funkcjami
    lines = read_log_file()
    if not lines:
        return {}

    errors = extract_errors_with_tracebacks(lines)
    error_count = len(errors)

    # 2. Logika walidacji (ustalamy status na podstawie liczby błędów)
    status = "ok"
    if error_count > 0:
        status = "error" if error_count > 5 else "warning"

    # 3. Budujemy finalny, zagnieżdżony słownik (Payload)
    payload = {
        "core": {
            "total_log_lines": len(lines),
            "generated_at": datetime.now().isoformat()
        },
        "logs": {
            "log_levels": extract_log_levels(lines),
            "modules_activity": extract_modules(lines),
            "errors": errors,
            "error_summary": summarize_errors(errors)
        },
        "validation": {
            "status": status,
            "error_count": error_count
        },
        "instructions": (
            "Przeanalizuj dostarczone logi systemowe. Skup się na błędach "
            "w sekcji 'errors'. Zidentyfikuj powtarzające się wzorce i "
            "zaproponuj rozwiązanie."
        )
    }

    logger.info(f"AI Analyzer: payload prepared with status: {status}")
    return payload