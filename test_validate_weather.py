import logging
from src.extract.weather import extract_phnom_penh
from src.transform.validate_weather import validate_weather_data

logging.basicConfig(level=logging.INFO)

data = extract_phnom_penh()
valid_data = validate_weather_data(data)

print(f"Final record count: {len(valid_data)}")
