import duckdb
import os
import logging

duck = duckdb.connect("data/weather.duckdb")
EXPORT_PATH = "data/export/weather.parquet"

def export_parquet():
    os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)

    logging.info(f"Exporting to {EXPORT_PATH}")

    duck.execute(f"""
        COPY weather TO '{EXPORT_PATH}' (FORMAT PARQUET)
    """)

    duck.close()