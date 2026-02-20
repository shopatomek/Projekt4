from app.ai_analyzer import build_ai_payload
import json

if __name__ == "__main__":
    payload = build_ai_payload()
    
    print("\n" + "🚀" * 15)
    print("DEBUG: AI PAYLOAD JSON")
    print("🚀" * 15 + "\n")
    
    # Wyświetlamy sformatowany JSON
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    print("\n" + "="*30)
    print(f"Total Raw Errors: {payload['logs'].get('total_errors_detected')}")
    print(f"Unique Error Types: {len(payload['logs'].get('unique_errors', []))}")
    print("="*30)