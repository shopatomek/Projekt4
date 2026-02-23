import os
import time
from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt
from app.logger import logger

# Ścieżka, którą udostępnimy dla n8n w docker-compose
SHARED_DIR = "shared_data"
SHARED_FILE = os.path.join(SHARED_DIR, "to_analyze.txt")


def run_pipeline():
    """
    Główny proces: Analiza logów -> Tworzenie promptu -> Zapis/Usuwanie pliku.
    """
    try:
        # 1. Pobranie danych z analizatora (zastępuje debug_ai_payload)
        payload = build_ai_payload()

        # 2. Przetworzenie danych na prompt (zastępuje debug_ai_adapter)
        prompt = build_prompt(payload)

        # 3. Zarządzanie plikiem komunikacyjnym (Most do n8n)
        if prompt:
            # Upewniamy się, że folder istnieje
            os.makedirs(SHARED_DIR, exist_ok=True)

            with open(SHARED_FILE, "w", encoding="utf-8") as f:
                f.write(prompt)
            logger.info(f"🚨 Wykryto błędy. Prompt zapisany w {SHARED_FILE}")
        else:
            # Jeśli system jest czysty, usuwamy stary plik, aby n8n nie wysłało go ponownie
            if os.path.exists(SHARED_FILE):
                os.remove(SHARED_FILE)
                logger.info("🧹 System czysty. Usunięto stary plik promptu.")
            else:
                logger.info("✅ System czysty. Brak nowych błędów do zgłoszenia.")

    except Exception as e:
        logger.error(f"❌ Krytyczny błąd w pipeline: {e}")


if __name__ == "__main__":
    logger.info("🚀 Agent monitorujący uruchomiony (interwał: 5 minut)...")

    try:
        while True:
            run_pipeline()

            # Czekaj przed kolejnym sprawdzeniem (300 sekund = 5 minut)
            time.sleep(300)

    except KeyboardInterrupt:
        logger.info("👋 Agent zatrzymany przez użytkownika.")
    except Exception as e:
        logger.error(f"💥 Agent przestał działać z powodu nieoczekiwanego błędu: {e}")
