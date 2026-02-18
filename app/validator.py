from app.logger import logger


def validate_data(parsed_data):
    logger.info("Starting data validation")
    validated = []
    for item in parsed_data:
        if item["age"] > 0:
            validated.append(item)
        else:
            logger.error(f"Invalid age for item {item}")
    logger.info(f"Validation finished, validated {len(validated)} items")
    return validated