import duckdb
import logging
from extract import extract
# from load import load
# from transform import transform

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
DB_PATH = "data/weather.duckdb"

def run_pipeline(city, year):
    logging.info(f"Starting ELT pipeline for {city} in {year}...")
    duck = duckdb.connect(DB_PATH)

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
        logging.info(f"Data for {city}, {year} already in DB. Pipeline terminated.")
        return
    
    todo = extract(city, year)

    logging.info("Successfully extracted, loaded, and transformed data.")