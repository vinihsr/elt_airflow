from extract import extract_car_data
from load import load_to_postgres

def run_pipeline():
    print("--- Starting OnCar Data Pipeline ---")
    print("Step 1: Extracting data from API...")
    df = extract_car_data() # Call the extraction

    if df is not None and not df.empty: # If it isn't NULL or empty, do:
        print("Step 2: Loading raw data into PostgreSQL...")
        load_to_postgres(df) # Call the loading
        print("--- Pipeline Finished Successfully ---")
    else:
        print("Pipeline aborted: No data found.")

if __name__ == "__main__": # Main function
    run_pipeline()