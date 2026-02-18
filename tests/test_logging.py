import os
import subprocess

LOG_FILE = "app.log"


def test_app_creates_log_file():
    # usuń log, jeśli istnieje (czysty start)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # uruchom aplikację
    subprocess.run(["python", "main.py"], check=True)

    # sprawdź czy plik logów powstał
    assert os.path.exists(LOG_FILE)


def test_log_contains_info_and_error():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.read()

    assert "INFO" in logs
    assert "ERROR" in logs
    assert "division by zero" in logs
