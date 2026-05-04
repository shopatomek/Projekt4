## testy manualne

python -m scripts.debug_ai_payload
python -m scripts.debug_ai_adapter -s
python -m scripts.debug_ai_client
python -m scripts.debug_ai_analyzer

## testy jednostkowe

python -m pytest tests/test_ai_client.py
python -m pytest tests/test_ai_analyzer.py
python -m pytest tests/test_ai_adapter.py
python -m pytest tests/test_logging.py

## Docker

docker-compose up --build
docker-compose up -d
docker logs -f projekt4

## Odśwież agenta jeżeli jeżeli kod python został zmieniony

Zatrzymaj wszystko: docker-compose down

Przebuduj obraz: docker-compose up --build -d
