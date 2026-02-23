def build_prompt(payload: dict) -> str:
    """
    Główna funkcja adaptera.
    Przyjmuje ulepszony kontrakt AI (payload z unikalnymi błędami)
    i zamienia go na czytelny prompt dla modelu językowego.
    """

    if not payload:
        return "No data available for analysis."

    # Używamy .get(), aby uniknąć KeyError, jeśli któraś sekcja by nie istniała
    core = payload.get("core", {})
    logs = payload.get("logs", {})
    validation = payload.get("validation", {})
    instructions = payload.get("instructions", "Analyze the logs and provide insights.")

    unique_errors = logs.get("unique_errors", [])

    lines = []

    # --- Kontekst systemowy ---
    lines.append("### SYSTEM CONTEXT")
    lines.append("=" * 18)
    lines.append(f"Status: {validation.get('status', 'UNKNOWN').upper()}")
    # ZMIANA: używamy nowej nazwy klucza z ai_analyzer
    lines.append(f"Total log lines analyzed: {core.get('total_log_lines_in_session', 0)}")
    # ZMIANA: używamy 'new_errors_found' zamiast 'total_errors_detected'
    lines.append(f"Total errors detected: {logs.get('new_errors_found', 0)}")
    lines.append(f"Session status: {core.get('session_status', 'N/A')}")
    lines.append(f"Generated at: {core.get('generated_at', 'N/A')}")
    lines.append("")

    # --- Aktywność modułów ---
    lines.append("### MODULE ACTIVITY")
    lines.append("=" * 18)
    modules = logs.get("modules_activity", {})
    if not modules:
        lines.append("No activity recorded.")
    for module, count in modules.items():
        lines.append(f"{module}: {count} events")
    lines.append("")

    # --- Analiza unikalnych błędów ---
    lines.append("### UNIQUE ERROR ANALYSIS")
    lines.append("=" * 25)

    if not unique_errors:
        lines.append("No critical errors found in the current session.")
    else:
        for idx, err_data in enumerate(unique_errors, start=1):
            lines.append(f"{idx}) ERROR: {err_data.get('message', 'No message')}")
            lines.append(f"   OCCURRENCES: {err_data.get('count', 1)}")

            traceback = err_data.get("sample_traceback", [])
            if traceback:
                lines.append("   SAMPLE TRACEBACK:")
                for tb in traceback:
                    lines.append(f"      {tb}")

            lines.append("-" * 30)

    lines.append("")

    # --- Instrukcja dla AI ---
    lines.append("### INSTRUCTIONS")
    lines.append("=" * 16)
    lines.append(instructions)

    return "\n".join(lines)
