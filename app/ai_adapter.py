def build_prompt(payload: dict) -> str:
    """
    Główna funkcja adaptera.
    Przyjmuje ulepszony kontrakt AI (payload z unikalnymi błędami) 
    i zamienia go na czytelny prompt.
    """

    if not payload:
        return "No data available for analysis."

    core = payload["core"]
    logs = payload["logs"]
    validation = payload["validation"]
    instructions = payload["instructions"]
    
    # Wyciągamy naszą nową listę unikalnych błędów
    unique_errors = logs.get("unique_errors", [])

    lines = []

    # --- Kontekst systemowy ---
    lines.append("SYSTEM CONTEXT")
    lines.append("=" * 14)
    lines.append(f"Status: {validation['status'].upper()}")
    lines.append(f"Total log lines analyzed: {core['total_log_lines']}")
    lines.append(f"Total errors detected: {logs.get('total_errors_detected', 0)}")
    lines.append(f"Generated at: {core['generated_at']}")
    lines.append("")

    # --- Aktywność modułów ---
    lines.append("MODULE ACTIVITY")
    lines.append("=" * 15)
    for module, count in logs["modules_activity"].items():
        lines.append(f"{module}: {count} events")
    lines.append("")

    # --- Analiza unikalnych błędów ---
    lines.append("UNIQUE ERROR ANALYSIS")
    lines.append("=" * 21)
    
    if not unique_errors:
        lines.append("No critical errors found in the analyzed period.")
    else:
        for idx, err_data in enumerate(unique_errors, start=1):
            # Wyświetlamy treść błędu i to, ile razy wystąpił
            lines.append(f"{idx}) ERROR: {err_data['message']}")
            lines.append(f"   OCCURRENCES: {err_data['count']}")
            
            if err_data['sample_traceback']:
                lines.append("   SAMPLE TRACEBACK:")
                for tb in err_data['sample_traceback']:
                    # Dodajemy wcięcie dla tracebacku, żeby prompt był czytelny
                    lines.append(f"      {tb}")
            
            # Dodajemy mały separator między różnymi typami błędów
            lines.append("-" * 30)

    lines.append("")

    # --- Instrukcja dla AI ---
    lines.append("INSTRUCTIONS")
    lines.append("=" * 12)
    lines.append(instructions)

    return "\n".join(lines)