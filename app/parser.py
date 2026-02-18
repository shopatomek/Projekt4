from app.logger import logger


def parse_data(raw_data):
    logger.info("Parser: start parsing data")
    parsed = []

    for idx, item in enumerate(raw_data, start=1):
        try:
            parsed_item = {
                "name": item["name"],
                "age": int(item["age"])  # może rzucić ValueError
            }
            parsed.append(parsed_item)
            logger.info(
                f"Parser: successfully parsed item {idx} -> {parsed_item}"
            )
        except Exception:
            logger.error(
                f"Parser: error parsing item {idx} -> {item}", exc_info=True
            )

    logger.info(f"Parser: finished, parsed {len(parsed)} items")
    return parsed
