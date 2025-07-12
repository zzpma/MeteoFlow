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
    all_data = []

    lat, lon = get_coordinates(city)
    print(f"Geocoded {city}: lat={lat}, lon={lon}")

    for month in range(1, 13):
        start_date = f"{year}-{month:02d}-01"

        if year == today.year and month == today.month:
            end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            last_day = calendar.monthrange(year, month)[1]
            end_date = f"{year}-{month:02d}-{last_day:02d}"

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
        data = response.json()

        if "daily" in data:
            for date, tmin, tmax in zip(
                data["daily"]["time"],
                data["daily"]["temperature_2m_min"],
                data["daily"]["temperature_2m_max"]
            ):
                all_data.append({
                    "city": city,
                    "date": date,
                    "temp_min": tmin,
                    "temp_max": tmax
                })
        else:
            print(f"⚠️ No daily data found for {city} {calendar.month_name[month]} {year}")
            
    return [(d["city"], d["date"], d["temp_min"], d["temp_max"]) for d in all_data]