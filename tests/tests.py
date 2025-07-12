import duckdb
import pandas as pd
import os

DB_PATH = "data/weather.duckdb"
PARQUET_PATH = "data/export/weather.parquet"

def test_duckdb():
    print("\n🔍 Testing DuckDB File...")
    if not os.path.exists(DB_PATH):
        print(f"❌ DuckDB file not found: {DB_PATH}")
        return
    
    con = duckdb.connect(DB_PATH)

    try:
        row_count = con.execute("SELECT COUNT(*) FROM weather").fetchone()[0]
        print(f"✅ Row count in weather table: {row_count}")

        print("\n👀 Sample records:")
        print(con.execute("SELECT * FROM weather LIMIT 5").fetchdf())

        print("\n📆 Date range per city:")
        print(con.execute("""
            SELECT city, MIN(date) AS start_date, MAX(date) AS end_date
            FROM weather GROUP BY city
        """).fetchdf())

        print("\n⚠️ Null check for temperature columns:")
        nulls = con.execute("""
            SELECT COUNT(*) FROM weather WHERE temp_min IS NULL OR temp_max IS NULL
        """).fetchone()[0]
        print(f"Found {nulls} records with NULL temperature values.")

    except Exception as e:
        print(f"❌ Error while querying DuckDB: {e}")
    finally:
        con.close()


def test_parquet():
    print("\n🔍 Testing Parquet File...")
    if not os.path.exists(PARQUET_PATH):
        print(f"❌ Parquet file not found: {PARQUET_PATH}")
        return
    
    try:
        df = pd.read_parquet(PARQUET_PATH)
        print(f"✅ Loaded parquet file: {PARQUET_PATH}")
        print(f"Total rows: {len(df)}")
        print("\n👀 Sample records:")
        print(df.head())

        print("\n📆 Date range per city:")
        print(df.groupby("city")["date"].agg(["min", "max"]))

        print("\n⚠️ Null check for temperature columns:")
        print(df[["temp_min", "temp_max"]].isnull().sum())

    except Exception as e:
        print(f"❌ Error while reading Parquet: {e}")


if __name__ == "__main__":
    test_duckdb()
    test_parquet()
