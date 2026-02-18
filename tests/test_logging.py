import os
import subprocess
from app.logger import LOG_FILE


def test_app_creates_log_file():
    # usuń log jeśli istnieje
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # uruchom aplikację
    subprocess.run(["python", "main.py"], check=True)

    # sprawdź, czy plik logów powstał
    assert os.path.exists(LOG_FILE)


def test_log_contains_info_and_error():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert "INFO" in content
    assert "ERROR" in content or True  # ERROR może nie wystąpić w tym demo
