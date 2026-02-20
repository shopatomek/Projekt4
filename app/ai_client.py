import time
import os
from app.logger import logger


class AIClient:
    def __init__(self, use_mock=True):
        self.use_mock = use_mock
        # Tu w przyszłości dodamy self.api_key = os.getenv("GEMINI_API_KEY")
        self.api_key = os.getenv("GEMINI_API_KEY")

    def get_analysis(self, prompt: str) -> str:
        """
        Wysyła prompt do AI i zwraca analizę. 
        Obecnie obsługuje tryb Mock dla testów.
        """
        logger.info(f"AI Client: Starting analysis (Mock mode: {self.use_mock})")

        if self.use_mock:
            return self._generate_mock_response()
        
        # Miejsce na realne połączenie z API (np. google-generativeai)
        return "Real API not implemented yet."

    def _generate_mock_response(self) -> str:
        """
        Symuluje inteligentną odpowiedź modelu AI.
        """
        time.sleep(1.5)  # Symulacja opóźnienia sieciowego
        
        analysis = (
            "### 🔍 Analiza Błędów Systemowych\n\n"
            "**Główne problemy:**\n"
            "1. **Błędy Typu (Parser):** Wykryto 39 wystąpień prób konwersji tekstu na liczbę (np. 'thirty'). "
            "Należy zaktualizować moduł Parser o funkcję mapującą liczebniki lub dodać lepszą walidację wejścia.\n"
            "2. **Błędy Biznesowe (Validator):** Wykryto 39 przypadków nieprawidłowego wieku (wartości <= 0). "
            "Sugerowane sprawdzenie źródła danych Scrapera.\n\n"
            "**Rekomendacja:** Wprowadzić blok `try-except` w `parser.py:12` z domyślną wartością 0."
        )
        return analysis

# Prosta funkcja pomocnicza do szybkiego testu


if __name__ == "__main__":
    client = AIClient(use_mock=True)
    print(client.get_analysis("Testowy prompt"))