from app.ai_analyzer import build_ai_payload
from app.ai_adapter import build_prompt


def test_build_prompt_returns_string():
    payload = build_ai_payload()
    prompt = build_prompt(payload)

    assert isinstance(prompt, str)
    assert "SYSTEM CONTEXT" in prompt
    assert "ERROR SUMMARY" in prompt
    assert "INSTRUCTIONS" in prompt