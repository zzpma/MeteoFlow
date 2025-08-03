import typer
import logging
from meteoflow.pipeline import run_pipeline
from meteoflow.export import export_parquet

app = typer.Typer(help="Weather ELT CLI")
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

@app.command("get")
def get(city: str, year: int):
    """
    Run the ELT pipeline for a city and year.
    """
    try:
        run_pipeline(city, year)
        logging.info("✅ Pipeline completed successfully.")
    except Exception as err:
        logging.error(f"❌ Operation failed with error: {err}")

@app.command("export")
def export():
    """
    Export weather data in DuckDB to a Parquet file.
    """
    try:
        export_parquet()
        logging.info("📦 Export completed successfully.")
    except Exception as err:
        logging.error(f"❌ Export failed with error: {err}")