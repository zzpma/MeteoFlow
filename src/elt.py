import logging

from extract import extract
# from load import load
# from transform import transform

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

print("Starting ELT pipeline...")

CITIES = [
    {"name": "Paris",     "lat": 48.8566, "lon": 2.3522},
    {"name": "Berlin",    "lat": 52.52,   "lon": 13.4050},
    {"name": "Madrid",    "lat": 40.4168, "lon": -3.7038},
    {"name": "Rome",      "lat": 41.9028, "lon": 12.4964},
    {"name": "Amsterdam", "lat": 52.3676, "lon": 4.9041},
]
YEAR = 2025
MONTH = 5

try:
	raw_weather_data = extract(CITIES, YEAR, MONTH)
	print(raw_weather_data)

	logging.info("Successfully extracted, loaded, and transformed data.")

except Exception as err:
	logging.error(f"Pipeline failed with error: {err}")