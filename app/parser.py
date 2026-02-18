from app.logger import logger


def scrape_data(raw_data):
    logger.info("Starting data parsing")
    parsed = []
    for item in raw_data:
        try:
            parsed_item = {
                "name": item["name"],
                "age": int(item["age"])  # może rzucić ValueError
            }
            parsed.append(parsed_item)
        except Exception as e:
            logger.error(f"Error parsing item {item}: {e}")
            logger.info(f"Parser finished, parsed {len(parsed)} items")
    return parsed