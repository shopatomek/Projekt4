# Wybieramy stabilną wersję Pythona
FROM python:3.11-slim

# Ustawiamy zmienną środowiskową, żeby logi od razu pojawiały się w konsoli
ENV PYTHONUNBUFFERED=1

# Ustalamy folder roboczy wewnątrz kontenera
WORKDIR /app

# Kopiujemy plik z bibliotekami i instalujemy je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy całą zawartość Twojego folderu do kontenera
COPY . .

# Tworzymy foldery, jeśli ich nie ma (choć kopia powinna je przenieść)
RUN mkdir -p logs shared_data

# Odpalamy skrypt
CMD ["python", "main.py"]