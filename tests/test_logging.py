import os
import logging
import pytest
from app.logger import logger, INTERNAL_LOG, APP_LOG


# --- TESTY ISTNIENIA PLIKÓW ---


def test_internal_log_file_exists():
    """internal.log musi istnieć po zaimportowaniu loggera."""
    assert os.path.exists(INTERNAL_LOG), f"Brak pliku: {INTERNAL_LOG}"


def test_app_log_file_exists():
    """app.log musi istnieć po zaimportowaniu loggera."""
    assert os.path.exists(APP_LOG), f"Brak pliku: {APP_LOG}"


# --- TESTY ZAPISU ---


def test_info_message_written_to_internal_log():
    """INFO trafia do internal.log."""
    marker = "TEST_INFO_INTERNAL_XYZ123"
    logger.info(marker)
    with open(INTERNAL_LOG, "r", encoding="utf-8") as f:
        content = f.read()
    assert marker in content


def test_error_message_written_to_internal_log():
    """ERROR trafia do internal.log."""
    marker = "TEST_ERROR_INTERNAL_XYZ123"
    logger.error(marker)
    with open(INTERNAL_LOG, "r", encoding="utf-8") as f:
        content = f.read()
    assert marker in content


def test_info_message_written_to_app_log():
    """INFO (bez słowa 'item') trafia do app.log."""
    marker = "TEST_INFO_APP_XYZ123"
    logger.info(marker)
    with open(APP_LOG, "r", encoding="utf-8") as f:
        content = f.read()
    assert marker in content


# --- TESTY FILTRA SmartCleanFilter ---


def test_item_info_filtered_from_app_log():
    """Linia INFO zawierająca 'item' NIE powinna trafiać do app.log."""
    marker = "TEST_FILTER_item_should_be_blocked_XYZ999"
    logger.info(marker)
    with open(APP_LOG, "r", encoding="utf-8") as f:
        content = f.read()
    assert marker not in content


def test_item_info_still_in_internal_log():
    """Linia INFO z 'item' MUSI być w internal.log mimo filtra."""
    marker = "TEST_FILTER_item_in_internal_XYZ999"
    logger.info(marker)
    with open(INTERNAL_LOG, "r", encoding="utf-8") as f:
        content = f.read()
    assert marker in content


# --- TESTY FORMATU LOGU ---


def test_log_format_contains_level():
    """Logi muszą zawierać poziom (INFO/ERROR) w formacie pipe-separated."""
    marker = "TEST_FORMAT_LEVEL_CHECK"
    logger.info(marker)
    with open(INTERNAL_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()
    matching = [l for l in lines if marker in l]
    assert len(matching) > 0
    assert "| INFO |" in matching[-1]


def test_log_format_contains_timestamp():
    """Każdy wpis musi zaczynać się od timestampu YYYY-MM-DD."""
    marker = "TEST_FORMAT_TIMESTAMP_CHECK"
    logger.info(marker)
    with open(INTERNAL_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()
    matching = [l for l in lines if marker in l]
    assert len(matching) > 0
    import re

    assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", matching[-1])
