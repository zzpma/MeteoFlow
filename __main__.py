import argparse
import logging
from src.pipeline import run_pipeline
from src.export import export_parquet

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def main():
    parser = argparse.ArgumentParser(description="Weather ELT CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: run
    run_parser = subparsers.add_parser("run", help="Run the ELT pipeline for a city and year")
    run_parser.add_argument("city", type=str, help="Name of the city (e.g. Paris)")
    run_parser.add_argument("year", type=int, help="Year to extract weather data for (e.g. 2024)")

    # Subcommand: export
    export_parser = subparsers.add_parser("export", help="Export weather data in DuckDB to a Parquet file")

    args = parser.parse_args()

    try:
        if args.command == "get":
            run_pipeline(args.city, args.year)
            logging.info("✅ Pipeline completed successfully.")

        elif args.command == "export":
            export_parquet()
            logging.info("📦 Export completed successfully.")

    except Exception as err:
        logging.error(f"❌ Operation failed with error: {err}")

if __name__ == "__main__":
    main()
