import os
import logging
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from src.extract.exchange_rate import extract_exchange_rate

# Load environment variables from .env
load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def validate_data(data: list[dict]) -> list[dict]:
    """Basic validation before loading."""
    if not data:
        raise ValueError("No data to load!")

    # Check for missing dates (critical for our unique constraint)
    for row in data:
        if row['date'] is None:
            raise ValueError("Found a row with a missing date!")

    logger.info(f"Validation passed for {len(data)} rows.")
    return data


def load_exchange_rate():
    # 1. Extract & Validate
    data = extract_exchange_rate()
    validated_data = validate_data(data)

    # 2. Connect to Database (using the external port 5435 from your host machine)
    # Note: We use localhost because this script runs on your laptop, not inside Docker.
    conn = psycopg2.connect(
        host="localhost",
        port=5435,
        dbname=os.getenv("WAREHOUSE_DB", "tourism_weather_dw"),
        user=os.getenv("WAREHOUSE_USER", "warehouse"),
        password=os.getenv("WAREHOUSE_PASS", "warehouse")
    )
    cursor = conn.cursor()

    # 3. Prepare the data as a list of tuples
    # We only extract the columns we need for the raw table
    values = [
        (
            # Convert pandas Timestamp to string
            row['date'].strftime('%Y-%m-%d'),
            str(row['purchase']),
            str(row['sale']),
            str(row['midpoint']),
            str(row['exchange_rate']),
            str(row['spread_market_day_x-1_over_oer_day_x_midpoint'])
        ) for row in validated_data
    ]

    # 4. The UPSERT Query
    # ON CONFLICT (date) DO UPDATE means: if the date exists, update the numbers.
    upsert_query = """
        INSERT INTO raw.exchange_rate_daily (date, purchase, sale, midpoint, exchange_rate, spread_market_day_x_1_over_oer_day_x_midpoint)
        VALUES %s
        ON CONFLICT (date) DO UPDATE SET
            purchase = EXCLUDED.purchase,
            sale = EXCLUDED.sale,
            midpoint = EXCLUDED.midpoint,
            exchange_rate = EXCLUDED.exchange_rate,
            spread_market_day_x_1_over_oer_day_x_midpoint = EXCLUDED.spread_market_day_x_1_over_oer_day_x_midpoint;
    """

    # execute_values is a fast way to bulk insert rows
    execute_values(cursor, upsert_query, values)
    conn.commit()

    logger.info(
        f"Successfully upserted {len(values)} rows into raw.exchange_rate_daily.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_exchange_rate()
