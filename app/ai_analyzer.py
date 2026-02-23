import os
import re
import json
import hashlib
from datetime import datetime
from collections import Counter
from app.logger import LOG_FILE, logger

# 1. KONFIGURACJA I STAŁE
TIMESTAMP_PATTERN = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}"
CACHE_FILE = "app/error_cache.json"


# 2. POMOCNICZE FUNKCJE CACHE (Zarządzanie pamięcią błędów)
def get_last_error_hash():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f).get("last_hash", "")
        except:
            return ""
    return ""


def save_error_hash(error_hash):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({"last_hash": error_hash}, f)
    except OSError as e:
        logger.error(f"Nie udało się zapisać cache do pliku: {e}")


# 3. FUNKCJE CZYTANIA I PARSOWANIA
def read_log_file():
    if not os.path.exists(LOG_FILE):
        logger.error("AI Analyzer: log file does not exist")
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    fresh_session_lines = []
    for line in reversed(all_lines):
        if "NEW SESSION STARTED" in line:
            break
        fresh_session_lines.append(line)

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
        is_new_entry = re.match(TIMESTAMP_PATTERN, line)

        if is_new_entry:
            if "| ERROR |" in line:
                current_error = {"message": line.strip(), "traceback": []}
                errors.append(current_error)
            else:
                current_error = None
        elif current_error is not None:
            clean_line = line.strip()
            if clean_line:
                current_error["traceback"].append(clean_line)
    return errors


def group_and_deduplicate_errors(errors):
    grouped = {}
    for err in errors:
        parts = err["message"].split("|")
        msg_key = parts[2].strip() if len(parts) >= 3 else err["message"]
        if msg_key not in grouped:
            grouped[msg_key] = {"message": msg_key, "count": 1, "sample_traceback": err["traceback"][:10]}
        else:
            grouped[msg_key]["count"] += 1
    return list(grouped.values())


# 4. GŁÓWNA LOGIKA BUDOWANIA PAYLOADU
def build_ai_payload():
    lines = read_log_file()
    if not lines:
        return {}

    raw_errors = extract_errors_with_tracebacks(lines)
    unique_errors = group_and_deduplicate_errors(raw_errors)

    # --- MECHANIZM DEDUPLIKACJI (Sprawdzamy czy błędy są NOWE) ---
    # Tworzymy unikalny klucz na podstawie treści błędów
    error_fingerprint = "".join(sorted([str(e["message"]) for e in unique_errors]))
    current_hash = hashlib.md5(error_fingerprint.encode()).hexdigest() if unique_errors else ""

    last_hash = get_last_error_hash()

    # Jeśli błędy są identyczne jak ostatnio i NIE są puste
    if current_hash == last_hash and unique_errors:
        logger.info("AI Analyzer: Te same błędy co w poprzednim cyklu. Pomijam raport.")
        return {}  # Zwracamy pusty słownik -> main.py uzna to za brak błędów do wysłania

    # Jeśli błędy są nowe (lub ich brak), aktualizujemy hash w pamięci
    save_error_hash(current_hash)

    error_count = len(raw_errors)
    status = "ok" if error_count == 0 else "warning" if error_count < 5 else "error"

    payload = {
        "core": {"total_log_lines_in_session": len(lines), "generated_at": datetime.now().isoformat(), "session_status": "fresh"},
        "logs": {"log_levels": extract_log_levels(lines), "modules_activity": extract_modules(lines), "unique_errors": unique_errors, "new_errors_found": error_count},
        "validation": {"status": status, "error_count": error_count},
        "instructions": "Przeanalizuj NOWE błędy i zaproponuj rozwiązanie.",
    }

    logger.info(f"AI Analyzer: Przygotowano payload. Nowe błędy: {error_count}")
    return payload
