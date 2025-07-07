import requests
import json
import calendar
import os
from datetime import datetime, timedelta

def extract(cities, year, month):
    # Calculate date range
    today = datetime.today()
    start_date = f"{year}-{month:02d}-01"

    if year == today.year and month == today.month:
        end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        label = f"until_{(today - timedelta(days=1)).strftime('%d')}"
    else:
        last_day = calendar.monthrange(year, month)[1]
        end_date = f"{year}-{month:02d}-{last_day:02d}"
        label = ""

    raw_data = []

    for city in cities:
        # Generate filename
        filename = f"data/raw/{city['name']}_{calendar.month_name[month]}_{year}"
        if label:
            filename += f"_until_{label}"
        filename += ".json"

        # Load data from file if it exists
        if os.path.exists(filename):
            print(f"Skipping {city['name']}: {filename} already exists.")
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        # Fetch data from API otherwise
        else:
            url = (
                f"https://archive-api.open-meteo.com/v1/archive?"
                f"latitude={city['lat']}"
                f"&longitude={city['lon']}"
                f"&start_date={start_date}"
                f"&end_date={end_date}"
                f"&daily=temperature_2m_min,temperature_2m_max"
                f"&timezone=Europe%2FBerlin"
            )

            response = requests.get(url)
            print(f"📡 Fetching {city['name']}... Status: {response.status_code}")

            data = response.json()

            # Save raw data
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"💾 Saved to: {filename}")

        raw_data.append({
            "city": city["name"],
            "data": data
        })

    return raw_data