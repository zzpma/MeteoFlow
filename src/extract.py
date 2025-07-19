import requests
import calendar
from datetime import datetime, timedelta

def get_coordinates(city):
    """Get latitude and longitude from city name using Open-Meteo Geocoding API."""
    url = (
        f"https://geocoding-api.open-meteo.com/v1/search?"
        f"name={city}"
        f"&count=1&language=en&format=json"
    )
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to geocode {city} (status {response.status_code})")
    
    results = response.json().get("results")
    if not results:
        raise Exception(f"No geocoding results found for '{city}'")

    return results[0]["latitude"], results[0]["longitude"]

def extract(city, year):
    """Extract weather data for a specific city and year."""
    today = datetime.today()
    year_data = []

    lat, lon = get_coordinates(city)
    print(f"Geocoded {city}: lat={lat}, lon={lon}")

    for month in range(1, 13):
        start_date = f"{year}-{month:02d}-01"
        end_date = (
            (today - timedelta(days=1)).strftime("%Y-%m-%d") 
            if year == today.year and month == today.month
            else f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}"
        )

        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={lat}"
            f"&longitude={lon}"
            f"&start_date={start_date}"
            f"&end_date={end_date}"
            f"&daily=temperature_2m_min,temperature_2m_max"
            f"&timezone=Europe%2FBerlin"
            )

        response = requests.get(url)
        print(f"📡 Fetching {city} {calendar.month_name[month]} {year}... Status: {response.status_code}")
        month_data = response.json()

        if "daily" not in month_data:
            raise Exception(f"No daily data found for {city} {calendar.month_name[month]} {year}")
        
        year_data.extend(
            (city, date, tmin, tmax)
            for date, tmin, tmax in zip(
                month_data["daily"]["time"],
                month_data["daily"]["temperature_2m_min"],
                month_data["daily"]["temperature_2m_max"]
            )
        )

    return year_data