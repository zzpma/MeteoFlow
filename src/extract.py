import requests
import calendar
from datetime import datetime, timedelta

def get_coordinates(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    response = requests.get(url)
    results = response.json().get("results")

    if not results:
        raise ValueError(f"City '{city_name}' not found via geocoding API")

    return results[0]["latitude"], results[0]["longitude"]

def extract(city_names, year):
    today = datetime.today()
    all_data = []

    for city in city_names:
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

            # Optionally save raw JSON
            # filename = f"data/raw/{city.lower()}_{calendar.month_name[month]}_{year}.json"
            # os.makedirs("data/raw", exist_ok=True)
            # with open(filename, "w", encoding="utf-8") as f:
            #     json.dump(data, f, indent=2)
            # print(f"💾 Saved to {filename}")

            all_data.append({
                "city": city,
                "month": month,
                "data": data
            })

    return all_data
