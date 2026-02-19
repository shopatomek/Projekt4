import os
import re
from collections import Counter, defaultdict
from app.logger import LOG_FILE, logger


def read_log_file():
    """
    Wczytuje cały plik logów do pamięci.

    Zwraca:
        list[str] – lista linii z pliku logów
    """
    if not os.path.exists(LOG_FILE):
        logger.error("AI Analyzer: log file does not exist")
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logger.info(f"AI Analyzer: loaded {len(lines)} log lines")
    return lines


def extract_log_levels(log_lines):
    """
    Zlicza poziomy logów (INFO, ERROR, WARNING itd.).

    Argumenty:
        log_lines (list[str])

    Zwraca:
        dict[str, int] – liczba wystąpień każdego poziomu logu
    """
    levels = Counter()

    for line in log_lines:
        match = re.search(r"\|\s(INFO|ERROR|WARNING|DEBUG)\s\|", line)
        if match:
            levels[match.group(1)] += 1

    return dict(levels)


def extract_modules(log_lines):
    """
    Przypisuje logi do modułów (Scraper / Parser / Validator).

    Wykorzystuje konwencję:
        'Scraper:', 'Parser:', 'Validator:'

    Zwraca:
        dict[str, int] – liczba logów na moduł
    """
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
    """
    Wyciąga błędy wraz z tracebackami.

    Traceback = pełna ścieżka błędu Pythona (linia po linii).

    Zwraca:
        list[dict] – lista błędów w formacie strukturalnym
    """
    errors = []
    current_error = None

    for line in log_lines:
        if "| ERROR |" in line:
            # Nowy błąd
            current_error = {
                "message": line.strip(),
                "traceback": []
            }
            errors.append(current_error)

        elif current_error and line.startswith("Traceback"):
            current_error["traceback"].append(line.strip())

        elif current_error and current_error["traceback"]:
            # Kolejne linie tracebacka
            current_error["traceback"].append(line.rstrip())

    return errors


def summarize_errors(errors):
    """
    Tworzy statystyki błędów – idealne wejście dla AI.

    Argumenty:
        errors (list[dict])

    Zwraca:
        dict – zagregowane informacje o błędach
    """
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
    Główna funkcja modułu.

    Składa pełny, uporządkowany raport,
    który w przyszłości trafi 1:1 do modelu AI.

    Zwraca:
        dict – gotowy payload dla AI
    """
    log_lines = read_log_file()

    if not log_lines:
        return {}

    payload = {
        "total_log_lines": len(log_lines),
        "log_levels": extract_log_levels(log_lines),
        "modules_activity": extract_modules(log_lines),
        "errors": extract_errors_with_tracebacks(log_lines),
        "error_summary": summarize_errors(
            extract_errors_with_tracebacks(log_lines)
        ),
    }

    logger.info("AI Analyzer: payload prepared successfully")
    return payload
