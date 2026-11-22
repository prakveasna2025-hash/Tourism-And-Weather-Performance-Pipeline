import os
import logging
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from src.extract.tourism import extract_tourism_data
from src.transform.validate_tourism import validate_tourism_data

load_dotenv()
logger = logging.getLogger(__name__)


def load_tourism_data():
    # 1. Extract & Validate
    raw_data = extract_tourism_data()
    validated_data = validate_tourism_data(raw_data)

    # 2. Connect to Database
    conn = psycopg2.connect(
        host="localhost", port=5435,
        dbname=os.getenv("WAREHOUSE_DB", "tourism_weather_dw"),
        user=os.getenv("WAREHOUSE_USER", "warehouse"),
        password=os.getenv("WAREHOUSE_PASS", "warehouse")
    )
    cursor = conn.cursor()

    # 3. Prepare values (year, months, number_of_tourists)
    values = [
        (row["year"], row["months"], row["number_of_tourists"])
        for row in validated_data
    ]

    # 4. Upsert (using the composite unique constraint we just added)
    upsert_query = """
        INSERT INTO raw.tourism_monthly (year, months, number_of_tourists)
        VALUES %s
        ON CONFLICT (year, months) DO UPDATE SET
            number_of_tourists = EXCLUDED.number_of_tourists;
    """

    execute_values(cursor, upsert_query, values)
    conn.commit()

    logger.info(
        f"Successfully upserted {len(values)} rows into raw.tourism_monthly.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_tourism_data()
