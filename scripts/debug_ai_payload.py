from app.ai_analyzer import build_ai_payload
import json

if __name__ == "__main__":
    payload = build_ai_payload()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
