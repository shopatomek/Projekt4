import json
from app.ai_analyzer import build_ai_payload

# DODANE: Importujemy Twoją logikę, żeby wygenerować błędy do pliku
from app.scraper import scrape_demo_data
from app.parser import parse_data
from app.validator import validate_data

if __name__ == "__main__":
    print("🔄 Wymuszam uruchomienie systemu, żeby wygenerować logi...")
    
    # KROK 1: Generowanie logów do pliku app.log
    data = scrape_demo_data()
    parsed = parse_data(data)
    validate_data(parsed)
    
    print("✅ Logi zapisane. Rozpoczynam analizę...\n")
    
    # KROK 2: Analiza logów z pliku
    payload = build_ai_payload()
    
    print("🚀" * 15)
    print("DEBUG: AI PAYLOAD JSON")
    print("🚀" * 15 + "\n")
    
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    print("\n" + "="*30)
    print(f"Total Raw Errors: {payload['logs'].get('total_errors_detected')}")
    print(f"Unique Errors: {len(payload['logs'].get('unique_errors', []))}")
    print("="*30)