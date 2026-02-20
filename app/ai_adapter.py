def build_prompt(payload: dict) -> str:
    """
    Główna funkcja adaptera.
    Przyjmuje kontrakt AI (payload) i zamienia go na tekstowy prompt
    gotowy do wysłania do modelu językowego.
    """

    if not payload:
        return "No data available for analysis."

    core = payload["core"]
    logs = payload["logs"]
    validation = payload["validation"]
    instructions = payload["instructions"]

    lines = []

    # --- Kontekst systemowy ---
    lines.append("SYSTEM CONTEXT")
    lines.append("=" * 14)
    lines.append(f"Status: {validation['status'].upper()}")
    lines.append(f"Total log lines: {core['total_log_lines']}")
    lines.append(f"Generated at: {core['generated_at']}")
    lines.append("")

    # --- Aktywność modułów ---
    lines.append("MODULE ACTIVITY")
    lines.append("=" * 15)
    for module, count in logs["modules_activity"].items():
        lines.append(f"{module}: {count} events")
    lines.append("")

    # --- Podsumowanie błędów ---
    lines.append("ERROR SUMMARY")
    lines.append("=" * 13)
    for error_type, count in logs["error_summary"].items():
        lines.append(f"{error_type}: {count}")
    lines.append("")

    # --- Szczegóły błędów ---
    lines.append("ERROR DETAILS")
    lines.append("=" * 13)

    for idx, error in enumerate(logs["errors"], start=1):
        lines.append(f"{idx}) {error['message']}")
        if error["traceback"]:
            lines.append("Traceback:")
            for tb in error["traceback"]:
                lines.append(f"  {tb}")
        lines.append("")

    # --- Instrukcja dla AI ---
    lines.append("INSTRUCTIONS")
    lines.append("=" * 12)
    lines.append(instructions)

    return "\n".join(lines)