from app.logger import logger


def parse_data(raw_data):
    logger.info("Parser: start parsing data")
    parsed = []

    for idx, item in enumerate(raw_data, start=1):
        try:
            # Próba konwersji wieku na int
            parsed_item = {"name": item["name"], "age": int(item["age"])}
            parsed.append(parsed_item)
            # To zostanie wycięte z app.log przez filtr "NoItemInfoFilter",
            # ale zostanie w kodzie do Twoich testów:
            logger.info(f"Parser: successfully parsed item {idx} -> {parsed_item}")

        except (ValueError, TypeError, KeyError):
            # USUNIĘTO: exc_info=True -> Traceback znika z logów.
            # Zostaje tylko czytelna linia ERROR.
            logger.error(f"Parser: error parsing item {idx} -> {item}")

    logger.info(f"Parser: finished, parsed {len(parsed)} items")
    return parsed
