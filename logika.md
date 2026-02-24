# 1️⃣ .venv/ – środowisko wirtualne

Co robi: izoluje Pythona i zainstalowane pakiety (np. pytest, requests).

Dlaczego potrzebne: nie brudzi systemowego Pythona i pozwala mieć spójne zależności.

.venv/Scripts/python.exe → interpreter, którego używasz.

Każdy terminal, w którym widzisz (.venv) oznacza, że jesteś w tym izolowanym środowisku.

# 2️⃣ app/ – Twój kod źródłowy (Core logic)

app/**init**.py

Co robi: mówi Pythonowi „app to pakiet”, więc można importować moduły z app.\*.

Zawartość: może być pusty, po prostu wskazuje, że katalog jest pakietem.

app/core.py

Co robi: zawiera logikę biznesową, np. funkcję add(a, b) — prosta, testowalna funkcja.

Dlaczego tu: kod produkcyjny trzymamy osobno od testów, żeby łatwo było go konteneryzować, integrować z n8n czy AI.

# 3️⃣ tests/ – testy jednostkowe

tests/test_core.py

Co robi: sprawdza funkcję add(a, b) z app/core.py.

Jak działa:

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(**file**), '..')))
from app.core import add

Linia sys.path.append(...) dodaje katalog główny projektu do listy ścieżek, żeby Python znalazł pakiet app.

Funkcja test_add() sprawdza, czy add(2, 3) daje 5.

tests/test_logging.py

Co robi: sprawdza logowanie w Twoim projekcie (czy plik logów powstaje, czy zawiera INFO i ERROR).

To Twój punkt wyjścia do „observability” — podstawa pod agenta AI, który będzie analizował logi.

# 4️⃣ main.py – punkt startowy aplikacji

Co robi: tutaj w przyszłości będziemy uruchamiać cały workflow: scraper → parser → validator → zapis logów.

Na razie może być minimalny:

from app.core import add

if **name** == "**main**":
print("Application started")
print("2 + 3 =", add(2, 3))

main.py → miejsce, które będzie odpalane w n8n lub w Dockerze później.

Tutaj będą integrowane wszystkie moduły i logika AI.

# 5️⃣ Jak moduły „się znajdują”

tests/test_core.py importuje add z app/core.py przez dodanie katalogu głównego (Projekt4/) do sys.path.

Python wtedy widzi:

Projekt4/ → szukaj modułów
└── app/core.py

Dzięki temu możesz testować bez Dockera lokalnie, a później wszystko spakować w kontenerze.

##

# ai_analyzer.py

### 🧠 Co ten moduł robi — krok po kroku (Feynman style)

## 1️⃣ read_log_file()

➡️ czyta logi

bierze logs/app.log

zamienia go na listę linii

NIE interpretuje jeszcze niczego

To jest „surowy sygnał” z systemu

## 2️⃣ extract_log_levels()

    Szuka tagów: Używa wyrażeń regularnych (re.search), aby znaleźć w tekście frazy

➡️ ile INFO / ERROR / WARNING

regex wyciąga poziom logu

liczy częstotliwość

Przykład wyniku:

```json
{
  "INFO": 42,
  "ERROR": 5
}
```

## 3️⃣ extract_modules()

➡️ który moduł generuje ile logów

    Kategoryzuje: Sprawdza, czy w linii tekstu pojawia się słowo kluczowe (np. "Scraper:"). Jeśli tak, przypisuje ten log do konkretnego modułu.

Scraper

Parser

Validator

Dzięki temu AI będzie mogło powiedzieć:

„Parser generuje 80% błędów — skup się tam”

## 4️⃣ extract_errors_with_tracebacks()

➡️ najważniejsza część

    Zbiera detale: To najbardziej zaawansowana funkcja. Gdy napotka linię z błędem, zaczyna "zbierać" wszystkie kolejne linie, które wyglądają jak Traceback (szczegóły błędu technicznego), aż do momentu pojawienia się kolejnego logu.

każdy ERROR

pełny traceback (linia po linii)

zero zgadywania

To jest złoto dla AI.

## 5️⃣ summarize_errors()

➡️ statystyka przyczyn

    Klasyfikuje błędy: Przegląda znalezione błędy i na podstawie słów kluczowych (np. "ValueError") grupuje je, tworząc krótką statystykę wystąpień.

ile ValueError

ile błędów walidacji

ile „inne”

To AI zamienia w:

„najczęstsza przyczyna awarii to …”

6️⃣ build_ai_payload()

➡️ składa wszystko w jeden obiekt
➡️ TO JEST JEDYNE WEJŚCIE DLA AI

    Menedżer: Uruchamia po kolei wszystkie powyższe funkcje i składa ich wyniki w jeden finalny obiekt JSON.

Przykład (skrót):

```json
{
"total_log_lines": 87,
"log_levels": {...},
"modules_activity": {...},
"error_summary": {...},
"errors": [...]
}
```

# ai_adapter

    Główna funkcja adaptera.
    Przyjmuje ulepszony kontrakt AI (payload z unikalnymi błędami)
    i zamienia go na czytelny prompt.

# 🤖 ai_client.py

Teraz, gdy mamy już "co wysłać", musimy zbudować "kuriera", który to wyśle i odbierze odpowiedź. Ponieważ jesteśmy na etapie budowy (i nie chcemy marnować kasy na API przy każdym teście), zaczniemy od Mocka.

## Struktura modułu app/ai_client.py:

Moduł ten będzie pośrednikiem między Twoją logiką a światem zewnętrznym (Gemini/OpenAI).

Klasa AIClient: Główny punkt styku.

Metoda get_analysis(prompt): Wysyła tekst do AI i zwraca odpowiedź.

Tryb MOCK: Jeśli flaga DEBUG lub USE_MOCK jest włączona, zamiast łączyć się z internetem, skrypt zwróci przygotowany wcześniej "udawany" tekst analizy.

## Co dokładnie zrobi ten moduł (krok po kroku):

### Krok 1: Przyjęcie Promptu – Pobiera surowy tekst wygenerowany przez ai_adapter.

### Krok 2: Decyzja (Mock vs Real) – Sprawdza zmienne środowiskowe (.env). Jeśli nie ma klucza API, przełącza się na Mocka.

### Krok 3: Symulacja "Myślenia" – W trybie Mocka doda krótkie opóźnienie (time.sleep), żeby symulować czas odpowiedzi serwera.

### Krok 4: Zwrot Wyniku – Zwróci ustrukturyzowaną odpowiedź, którą potem n8n lub Twój skrypt wyśle na Slacka/E-mail.

# Architektura i Przepływ Danych (Data Flow)

W projekcie wprowadzono ścisły podział ról, aby uniknąć zamieszania przy analizie błędów. Kluczowym pojęciem jest DATA PERSISTENCE (Trwałość danych) – oznacza to, że informacje nie znikają po zamknięciu programu, lecz są składowane w pliku app.log. Analizator nie zgaduje, co jest w kodzie; on analizuje tylko to, co zostało fizycznie zapisane na dysku.

# 1. Moduły i ich funkcje:

Scraper (scraper.py): Źródło danych. Generuje surową listę informacji (np. o użytkownikach). To tutaj powstają błędy, które chcemy śledzić.

Parser & Validator (parser.py, validator.py): Filtry. Przetwarzają dane ze Scrapera i jeśli napotkają problem (np. ujemny wiek), wysyłają komunikat do Loggera.

Logger (logger.py): Notariusz. Zapisuje każdy ruch systemu do pliku app.log. To jedyne źródło prawdy dla AI.

AI Analyzer (ai_analyzer.py): Czytelnik. Przeszukuje app.log. Dzięki nowej zmianie potrafi zignorować stare wpisy i skupić się tylko na bieżącej sesji (od ostatniego znacznika "NEW SESSION").

AI Adapter (ai_adapter.py): Tłumacz. Zamienia suche dane statystyczne z Analizatora na czytelny dla AI prompt (instrukcję).

AI Client (ai_client.py): Posłaniec. Wysyła prompt do modelu AI i odbiera gotową analizę.

# 2. Schemat przepływu (Data Flow):

Project Data Flow and Architecture Documentation
The system architecture is based on the principle of Data Persistence. This ensures that the analysis is always performed on verified, historical facts recorded in the log files, rather than volatile in-memory states.

## Data Flow Sequence

1. Execution Phase: The process is initiated by calling the run_pipeline() function (within main.py or debug scripts). This acts as the primary engine driving the entire data cycle.

2. Registration Phase: At the start of each execution, a NEW SESSION STARTED marker is injected into the logs via app/logger.py. This serves as a physical separator within the app.log file to distinguish between historical data and the current test session.

3. Generation Phase: Data is retrieved by app/scraper.py and passed through app/parser.py and app/validator.py. Any discrepancies (e.g., type mismatches or range errors) are captured and recorded as ERROR entries.

4. Persistence Phase: All system activities and errors are stored in app.log. This file serves as the "single source of truth" for the subsequent analysis.

5. Extraction Phase: app/ai_analyzer.py performs a reverse-read of app.log, stopping at the most recent NEW SESSION STARTED marker. This ensures that only relevant, fresh data is processed, effectively eliminating noise from previous runs.

6. Adaptation Phase: Extracted statistics are processed by app/ai_adapter.py, which transforms raw counts and tracebacks into a structured "Prompt" containing sections like SYSTEM CONTEXT and UNIQUE ERROR ANALYSIS.

7. Analysis Phase: The finalized prompt is delivered to app/ai_client.py, where the AI model (or a dynamic mock) generates a human-readable report with actionable insights.
