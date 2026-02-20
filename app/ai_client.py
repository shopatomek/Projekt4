import time
import os
import re
from app.logger import logger


class AIClient:
    def __init__(self, use_mock=True):
        self.use_mock = use_mock
        # Przygotowane pod przyszłe API
        self.api_key = os.getenv("GEMINI_API_KEY")

    def get_analysis(self, prompt: str) -> str:
        """
        Wysyła prompt do AI i zwraca analizę.
        W trybie Mock analizuje prompt lokalnie, by zwrócić spójne dane.
        """
        logger.info(f"AI Client: Starting analysis (Mock mode: {self.use_mock})")

        if self.use_mock:
            return self._generate_mock_response(prompt)

        return "Real API not implemented yet. Use GEMINI_API_KEY and set use_mock=False."

    def _generate_mock_response(self, prompt: str) -> str:
        """
        Dynamiczny Mock: wyciąga dane z promptu i buduje realistyczną odpowiedź.
        """
        time.sleep(1.5)  # Symulacja pracy modelu AI

        # Ekstrakcja danych z promptu przy pomocy Regex
        # Szukamy liczby błędów (format z naszego ai_adaptera)
        total_errors_match = re.search(r"TOTAL ERRORS:\s*(\d+)", prompt)
        unique_types_match = re.search(r"UNIQUE ERROR TYPES:\s*(\d+)", prompt)

        total_errors = total_errors_match.group(1) if total_errors_match else "0"
        unique_types = unique_types_match.group(1) if unique_types_match else "0"

        # Budowanie dynamicznej odpowiedzi
        analysis = (
            "### 🤖 [Dynamic Mock] Analiza Błędów Systemowych\n\n"
            f"**Podsumowanie detekcji:**\n"
            f"W aktualnej sesji system wykrył łącznie **{total_errors}** wystąpień błędów, "
            f"sklasyfikowanych jako **{unique_types}** unikalne typy problemów.\n\n"
            "**Główne spostrzeżenia:**\n"
            "1. **Błędy w module Parser:** Większość problemów wynika z nieoczekiwanego formatu danych (np. tekst zamiast liczb).\n"
            "2. **Walidacja Biznesowa:** Wykryto rekordy z niepoprawnymi wartościami wieku, co sugeruje błędy w źródle danych.\n\n"
            "**Rekomendacja Inżynierska:**\n"
            "Należy zaimplementować bezpieczne rzutowanie typów w `parser.py` oraz dodać warunek `if age > 0` "
            "zanim dane trafią do dalszych etapów przetwarzania."
        )

        if int(total_errors) == 0:
            analysis = "### 🤖 [Dynamic Mock] Analiza: Status OK\n\nSystem działa poprawnie. Nie wykryto żadnych anomalii w logach."

        return analysis


if __name__ == "__main__":
    # Test lokalny - symulujemy prompt jaki wypluwa ai_adapter
    client = AIClient(use_mock=True)
    fake_prompt = """
    [SYSTEM CONTEXT] ...
    TOTAL ERRORS: 12
    UNIQUE ERROR TYPES: 3
    ...
    """
    print(client.get_analysis(fake_prompt))
