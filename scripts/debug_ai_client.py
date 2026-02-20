from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt
from app.ai_client import AIClient


def debug_full_flow():
    print("🔄 KROK 1: Generowanie Payload...")
    payload = build_ai_payload()
    
    print("🔄 KROK 2: Budowanie Promptu...")
    prompt = build_prompt(payload)
    
    print("🔄 KROK 3: Wysyłka do AI (MOCK)...")
    client = AIClient(use_mock=True)
    response = client.get_analysis(prompt)
    
    print("\n" + "✨" * 10)
    print("ODPOWIEDŹ AI:")
    print("✨" * 10)
    print(response)


if __name__ == "__main__":
    debug_full_flow()