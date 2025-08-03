import duckdb
import pandas as pd
import logging
from src.extract import extract

DB_PATH = "data/weather.duckdb"
duck = duckdb.connect(DB_PATH)

def run_pipeline(city, year):
    logging.info(f"Starting ELT pipeline for {city} in {year}...")

    duck.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT,
            date DATE,
            temp_min DOUBLE,
            temp_max DOUBLE
        )
    """)
    
    data_exists = duck.execute("""
        SELECT 1 FROM weather 
        WHERE city = ? AND strftime('%Y', date) = ?
        LIMIT 1
    """, (city, str(year))).fetchone()

    if data_exists:
        logging.warning(f"Data for {city}, {year} already in DB. Pipeline terminated.")
        return
    
    data = extract(city, year)

    if not data:
        logging.warning("No data to load.")
        return

    duck.register("data", pd.DataFrame(data, columns=["city", "date", "temp_min", "temp_max"]))
    duck.execute("""
        INSERT INTO weather 
        SELECT city, date, temp_min, temp_max FROM data
    """)
    logging.info(f"Loaded data into DB ({DB_PATH})")

    duck.close()