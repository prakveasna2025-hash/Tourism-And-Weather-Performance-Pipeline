from airflow.decorators import dag, task
from datetime import datetime
import logging

# Import our custom code from src/
from src.extract.weather import extract_weather_city, CITIES
from src.transform.validate_weather import validate_weather_data
from src.load.load_weather import load_weather_data

logger = logging.getLogger(__name__)

# Define the config as a list of dictionaries for Airflow to map over
CITY_CONFIGS = [
    {"name": "Phnom Penh", "lat": 11.5564, "lon": 104.9282},
    {"name": "Siem Reap", "lat": 13.3671, "lon": 103.8448},
    {"name": "Sihanoukville", "lat": 10.6253, "lon": 103.5234}
]


@dag(
    dag_id="weather_pipeline_multi_city",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # We will trigger this manually for now
    catchup=False,
    tags=["weather", "multi-city"]
)
def weather_pipeline():

    @task
    def extract(city_config: dict):
        return extract_weather_city(city_config["name"], city_config["lat"], city_config["lon"])

    @task
    def validate(data: list[dict]):
        return validate_weather_data(data)

    @task
    def load(data: list[dict]):
        load_weather_data(data)

    # ★ TASK 1 & 2: DYNAMIC TASK MAPPING
    # We pass the entire list of city configs. Airflow will spin up 1 task per city.
    extracted_data = extract.expand(city_config=CITY_CONFIGS)

    # The validate and load tasks automatically map over the outputs of the previous tasks
    validated_data = validate.expand(data=extracted_data)
    load.expand(data=validated_data)


# Instantiate the DAG
weather_pipeline()
