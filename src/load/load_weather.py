import os
import logging
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from src.extract.weather import extract_all_weather
from src.transform.validate_weather import validate_weather_data

load_dotenv()
logger = logging.getLogger(__name__)


def load_weather_data(validated_data: list[dict]):
    # 1. Extract & Validate
    raw_data = extract_all_weather()
    validated_data = validate_weather_data(raw_data)

    # 2. Connect to Database
    conn = psycopg2.connect(
        host=os.getenv("WAREHOUSE_HOST", "postgres-warehouse"),
        port=os.getenv("WAREHOUSE_PORT", "5432"),
        dbname=os.getenv("WAREHOUSE_DB", "tourism_weather_dw"),
        user=os.getenv("WAREHOUSE_USER", "warehouse"),
        password=os.getenv("WAREHOUSE_PASS", "warehouse")
    )
    cursor = conn.cursor()

    # 3. Prepare values (cast floats to string for raw TEXT columns)
    values = [
        (
            row["city"],
            row["time"],
            str(row["temperature_2m_mean"]),
            str(row["precipitation_sum"]),
            str(row["relative_humidity_2m_mean"]),
            str(row["wind_speed_10m_max"])
        ) for row in validated_data
    ]

    # 4. Upsert using the composite unique constraint (city, time)
    upsert_query = """
        INSERT INTO raw.weather_daily (city, time, temperature_2m_mean, precipitation_sum, relative_humidity_2m_mean, wind_speed_10m_max)
        VALUES %s
        ON CONFLICT (city, time) DO UPDATE SET
            temperature_2m_mean = EXCLUDED.temperature_2m_mean,
            precipitation_sum = EXCLUDED.precipitation_sum,
            relative_humidity_2m_mean = EXCLUDED.relative_humidity_2m_mean,
            wind_speed_10m_max = EXCLUDED.wind_speed_10m_max;
    """

    execute_values(cursor, upsert_query, values)
    conn.commit()

    logger.info(
        f"Successfully upserted {len(values)} rows into raw.weather_daily.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from src.extract.weather import extract_all_weather
    from src.transform.validate_weather import validate_weather_data
    raw_data = extract_all_weather()
    valid_data = validate_weather_data(raw_data)
    load_weather_data(valid_data)
