from src.pipeline import run_pipeline
import argparse
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def main():
    parser = argparse.ArgumentParser(description="Run the ELT pipeline for a given city and year.")
    parser.add_argument("city", type=str, help="Name of the city (e.g. Paris)")
    parser.add_argument("year", type=int, help="Year to extract weather data for (e.g. 2024)")
    args = parser.parse_args()
    
    try:
        run_pipeline(args.city, args.year)
        logging.info("Successfully extracted, loaded, and transformed data.")
        
    except Exception as err:
        logging.error(f"Pipeline failed with error: {err}")

if __name__ == "__main__":
    main()