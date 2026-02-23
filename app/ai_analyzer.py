import os
import re
from datetime import datetime
from collections import Counter
from app.logger import LOG_FILE, logger

# Regex do wykrywania początku nowej linii logu (timestamp)
TIMESTAMP_PATTERN = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}"


def read_log_file():
    if not os.path.exists(LOG_FILE):
        logger.error("AI Analyzer: log file does not exist")
        return []

    all_lines = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    # Szukamy ostatniej sesji od końca pliku
    fresh_session_lines = []
    for line in reversed(all_lines):
        if "NEW SESSION STARTED" in line:
            break
        fresh_session_lines.append(line)

    # Odwracamy z powrotem, żeby zachować chronologię
    return fresh_session_lines[::-1]


def extract_log_levels(log_lines):
    levels = Counter()
    for line in log_lines:
        match = re.search(r"\|\s(INFO|ERROR|WARNING|DEBUG)\s\|", line)
        if match:
            levels[match.group(1)] += 1
    return dict(levels)


def extract_modules(log_lines):
    modules = Counter()
    for line in log_lines:
        for mod in ["Scraper", "Parser", "Validator"]:
            if f"{mod}:" in line:
                modules[mod] += 1
    return dict(modules)


def extract_errors_with_tracebacks(log_lines):
    errors = []
    current_error = None

    for line in log_lines:
        is_new_log_entry = re.match(TIMESTAMP_PATTERN, line)

        if is_new_log_entry:
            if "| ERROR |" in line:
                current_error = {"message": line.strip(), "traceback": []}
                errors.append(current_error)
            else:
                # Jeśli napotkamy INFO/WARNING, "odcinamy" bieżący błąd,
                # by tracebacki nie wyciekały do innych wpisów.
                current_error = None
        else:
            # Tutaj linter sypał błędem.
            # Sprawdzamy czy current_error nie jest None i czy to słownik.
            if current_error is not None:
                clean_line = line.strip()
                if clean_line:
                    current_error["traceback"].append(clean_line)

    return errors
    """
    Wyciąga błędy, ale zatrzymuje się, gdy napotka nową linię logu (np. INFO).
    Eliminuje to 'szum' w tracebackach.
    """
    errors = []
    current_error = None

    for line in log_lines:
        # Sprawdzamy, czy linia zaczyna się od daty (początek nowego logu)
        is_new_log_entry = re.match(TIMESTAMP_PATTERN, line)

        if is_new_log_entry:
            if "| ERROR |" in line:
                # Rozpoczynamy zbieranie nowego błędu
                current_error = {"message": line.strip(), "traceback": []}
                errors.append(current_error)
            else:
                # To jest nowy log, ale NIE błąd (np. INFO) ->
                # kończymy zbieranie poprzedniego błędu (jeśli był)
                pass
        else:
            # Linia nie ma daty, więc jest kontynuacją (Traceback lub dane)
            if current_error:
                # Dodajemy tylko jeśli nie jest pustą linią
                clean_line = line.strip()
                if clean_line:
                    current_error["traceback"].append(clean_line)

    return errors


def group_and_deduplicate_errors(errors):
    """
    Zmienia listę 65 błędów w krótką listę unikalnych problemów z licznikiem.
    """
    grouped = {}

    for err in errors:

        parts = err["message"].split("|")
        msg_key = parts[2].strip() if len(parts) >= 3 else err["message"]

        if msg_key not in grouped:
            grouped[msg_key] = {"message": msg_key, "count": 1, "sample_traceback": err["traceback"][:10]}
        else:
            grouped[msg_key]["count"] += 1

    return list(grouped.values())


def build_ai_payload():
    # Pobieramy tylko linie z OSTATNIEJ sesji (dzięki naszej nowej funkcji read_log_file)
    lines = read_log_file()
    if not lines:
        return {"validation": {"status": "ok", "error_count": 0}, "message": "No data found in the current session."}

    # Te funkcje teraz dostają tylko świeże linie!
    raw_errors = extract_errors_with_tracebacks(lines)
    unique_errors = group_and_deduplicate_errors(raw_errors)

    error_count = len(raw_errors)

    # Logika statusu tylko dla TEJ sesji
    if error_count == 0:
        status = "ok"
    elif error_count < 5:
        status = "warning"
    else:
        status = "error"

    payload = {
        "core": {"total_log_lines_in_session": len(lines), "generated_at": datetime.now().isoformat(), "session_status": "fresh"},  # Informacja, że to nowości
        "logs": {"log_levels": extract_log_levels(lines), "modules_activity": extract_modules(lines), "unique_errors": unique_errors, "new_errors_found": error_count},  # To są Twoje "nowe błędy"
        "validation": {"status": status, "error_count": error_count},
        "instructions": "Przeanalizuj NOWE błędy z bieżącej sesji i zaproponuj rozwiązanie.",
    }

    logger.info(f"AI Analyzer: Session payload ready. New errors: {error_count}")
    return payload
