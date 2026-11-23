import logging
from src.utils.http_client import fetch_json

logger = logging.getLogger(__name__)


def extract_weather_city(city_name: str, lat: float, lon: float) -> list[dict]:
    """
    Extracts historical weather data for a single city and reshapes it into rows.
    """
    base_url = "https://archive-api.open-meteo.com/v1/archive"

    # 1. Define the API parameters
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2019-01-01",
        "end_date": "2023-12-31",
        "daily": "temperature_2m_mean,precipitation_sum,relative_humidity_2m_mean,wind_speed_10m_max",
        "timezone": "Asia/Phnom_Penh"
    }

    logger.info(f"Fetching weather data for {city_name}...")

    # 2. Call the API using our custom HTTP Client
    response = fetch_json(base_url, params=params)

    # 3. Extract the daily columnar data
    daily_data = response.get("daily", {})
    dates = daily_data.get("time", [])

    # 4. Transpose the arrays into a list of row dictionaries
    rows = []
    for i in range(len(dates)):
        row = {
            "city": city_name,
            "time": dates[i],
            "temperature_2m_mean": daily_data["temperature_2m_mean"][i],
            "precipitation_sum": daily_data["precipitation_sum"][i],
            "relative_humidity_2m_mean": daily_data["relative_humidity_2m_mean"][i],
            "wind_speed_10m_max": daily_data["wind_speed_10m_max"][i]
        }
        rows.append(row)

    logger.info(f"Successfully parsed {len(rows)} days for {city_name}.")
    return rows


def extract_phnom_penh() -> list[dict]:
    """Wrapper to extract just Phnom Penh."""
    return extract_weather_city("Phnom Penh", 11.5564, 104.9282)
