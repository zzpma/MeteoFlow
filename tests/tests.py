import duckdb
import os

DB_PATH = "data/weather.duckdb"
PARQUET_PATH = "data/export/weather.parquet"

def test_duckdb():
    print("\n🔍 Testing DuckDB File...")
    if not os.path.exists(DB_PATH):
        print(f"❌ DuckDB file not found: {DB_PATH}")
        return
    
    con = duckdb.connect(DB_PATH)
    test_weather_table(con, "database table")
    con.close()

def test_parquet():
    print("\n🔍 Testing Parquet File...")
    if not os.path.exists(PARQUET_PATH):
        print(f"❌ Parquet file not found: {PARQUET_PATH}")
        return
    
    con = duckdb.connect()  # In-memory database
    test_weather_table(con, "parquet file", f"FROM '{PARQUET_PATH}'")
    con.close()

def test_weather_table(con, source_name, from_clause="FROM weather"):
    try:
        # Row count
        row_count = con.execute(f"SELECT COUNT(*) {from_clause}").fetchone()[0]
        print(f"✅ Row count in {source_name}: {row_count}")

        # Sample records
        print(f"\n👀 Sample records from {source_name}:")
        print(con.execute(f"SELECT * {from_clause} LIMIT 5").fetchdf())

        # Date range per city
        print(f"\n📆 Date range per city in {source_name}:")
        print(con.execute(f"""
            SELECT city, MIN(date) AS start_date, MAX(date) AS end_date
            {from_clause} GROUP BY city
        """).fetchdf())

        # Null check
        print(f"\n⚠️ Null check for temperature columns in {source_name}:")
        nulls = con.execute(f"""
            SELECT 
                SUM(CASE WHEN temp_min IS NULL THEN 1 ELSE 0 END) AS null_temp_min,
                SUM(CASE WHEN temp_max IS NULL THEN 1 ELSE 0 END) AS null_temp_max
            {from_clause}
        """).fetchone()
        print(f"Found {nulls[0]} NULL temp_min and {nulls[1]} NULL temp_max values")

        # Basic stats
        print(f"\n📊 Temperature stats in {source_name}:")
        print(con.execute(f"""
            SELECT 
                AVG(temp_min) AS avg_temp_min,
                AVG(temp_max) AS avg_temp_max,
                MIN(temp_min) AS min_temp,
                MAX(temp_max) AS max_temp
            {from_clause}
        """).fetchdf())

    except Exception as e:
        print(f"❌ Error while testing {source_name}: {e}")

if __name__ == "__main__":
    test_duckdb()
    test_parquet()