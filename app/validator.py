from app.logger import logger


def validate_data(parsed_data):
    logger.info("Validator: start validation")
    validated = []

    for idx, item in enumerate(parsed_data, start=1):
        try:
            # Sprawdzamy wiek - bezpiecznie
            if item["age"] > 0:
                validated.append(item)
                # To zostanie w kodzie, ale filtr NoItemInfoFilter wytnie to z app.log
                logger.info(f"Validator: item {idx} valid -> {item}")
            else:
                # To zostanie zapisane w app.log, bo to ERROR
                logger.error(f"Validator: invalid age for item {idx} -> {item}")

        except KeyError:
            # Obsługa przypadku, gdyby Parser przepuścił coś bez klucza "age"
            logger.error(f"Validator: missing 'age' key in item {idx} -> {item}")
        except Exception as e:
            # Ogólny błąd, ale bez tracebacku (brak exc_info)
            logger.error(f"Validator: unexpected error at item {idx} -> {e}")

    logger.info(f"Validator: finished, validated {len(validated)} items")
    return validated
