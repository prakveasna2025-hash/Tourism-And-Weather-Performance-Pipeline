import logging
from src.utils.http_client import fetch_json

logger = logging.getLogger(__name__)
basicConfig = logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def extract_tourism_data() -> list[dict]:
    """
    Extracts tourism data from the MEF Data EF API, handling pagination.
    """
    base_url = "https://data.mef.gov.kh/api/v1/public-datasets/pd_6715e15d40cc5500017936e5/json"

    all_items = []
    page = 1
    total_pages = 1

    logger.info("Starting tourism data extraction from API...")

    # 1. Pagination Loop
    while page <= total_pages:
        # We use the fetch_json utility we built on Day 8 (handles retries/timeouts)
        response = fetch_json(
            base_url, params={"page": page, "page_size": 100})

        # Grab the items and the total_pages count from the JSON response
        items = response.get("items", [])
        all_items.extend(items)
        total_pages = response.get("total_pages", 1)

        page += 1

    logger.info(f"Fetched {len(all_items)} raw records from API.")

    # 2. Clean fields and convert types
    cleaned_data = []
    for row in all_items:
        # The API returns floats (e.g., 2018.0). We cast to int, then to string.
        year_str = str(int(row["year"])) if row["year"] is not None else None
        tourists_str = str(int(row["number_of_tourists"])
                           ) if row["number_of_tourists"] is not None else None
        month_str = str(row["months"]).strip(
        ) if row["months"] is not None else None

        cleaned_data.append({
            "year": year_str,
            "months": month_str,
            "number_of_tourists": tourists_str
        })

    logger.info(f"Successfully cleaned {len(cleaned_data)} tourism records.")
    return cleaned_data
