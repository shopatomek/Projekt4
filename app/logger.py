import logging
import os

# Upewnij się, że katalog "logs" istnieje
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
# Utwórz logger dla tego modułu
logger = logging.getLogger(__name__)

