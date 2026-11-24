import logging

logger = logging.getLogger(__name__)


def validate_weather_data(data: list[dict]) -> list[dict]:
    """
    Validates weather data for missing values and physical impossibilities.
    """
    if not data:
        raise ValueError("No weather data to validate!")

    logger.info(f"Starting validation for {len(data)} weather records...")

    validated_data = []

    for row in data:
        # 1. Check for missing values (API glitches)
        if any(v is None for v in row.values()):
            logger.warning(f"Skipping row due to missing values: {row}")
            continue

        temp = row["temperature_2m_mean"]
        precip = row["precipitation_sum"]
        humidity = row["relative_humidity_2m_mean"]
        wind = row["wind_speed_10m_max"]

        # 2. Physical boundary checks
        # Precipitation and wind cannot be negative
        if precip < 0 or wind < 0:
            logger.warning(f"Skipping row with negative weather values: {row}")
            continue

        # Humidity must be between 0 and 100%
        if humidity < 0 or humidity > 100:
            logger.warning(f"Skipping row with impossible humidity: {row}")
            continue

        # Cambodia is tropical; temps below 10°C or above 45°C are sensor errors
        if temp < 10 or temp > 45:
            logger.warning(
                f"Skipping row with unrealistic temperature for Cambodia: {row}")
            continue

        # If it passes all checks, keep it
        validated_data.append(row)

    logger.info(
        f"Validation complete. {len(validated_data)} valid records ready for loading.")
    return validated_data
