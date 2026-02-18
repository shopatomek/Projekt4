from app.logger import logger


def validate_data(parsed_data):
    logger.info("Validator: start validation")
    validated = []

    for idx, item in enumerate(parsed_data, start=1):
        if item["age"] > 0:
            validated.append(item)
            logger.info(f"Validator: item {idx} valid -> {item}")
        else:
            logger.error(f"Validator: invalid age for item {idx} -> {item}")

    logger.info(f"Validator: finished, validated {len(validated)} items")
    return validated
