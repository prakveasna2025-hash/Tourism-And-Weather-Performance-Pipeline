import logging
from src.utils.http_client import fetch_json

logger = logging.getLogger(__name__)

# 🌟 TASK 2: The City Config
# This dictionary centralizes our cities. To add a new one, just add a line here.
CITIES = {
    "Phnom Penh": {"lat": 11.5564, "lon": 104.9282},
    "Siem Reap": {"lat": 13.3671, "lon": 103.8448},
    "Sihanoukville": {"lat": 10.6253, "lon": 103.5234}
}


def extract_weather_city(city_name: str, lat: float, lon: float) -> list[dict]:
    """
    Extracts historical weather data for a single city and reshapes it into rows.
    """
    base_url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2019-01-01",
        "end_date": "2023-12-31",
        "daily": "temperature_2m_mean,precipitation_sum,relative_humidity_2m_mean,wind_speed_10m_max",
        "timezone": "Asia/Phnom_Penh"
    }

    logger.info(f"Fetching weather data for {city_name}...")
    response = fetch_json(base_url, params=params)

    daily_data = response.get("daily", {})
    dates = daily_data.get("time", [])

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

# 🌟 TASK 1: The Refactored Extractor


def extract_all_weather() -> list[dict]:
    """
    Loops through the CITIES config and extracts weather data for all of them.
    """
    all_weather_data = []

    for city_name, coords in CITIES.items():
        city_data = extract_weather_city(
            city_name, coords["lat"], coords["lon"])
        all_weather_data.extend(city_data)

    return all_weather_data
