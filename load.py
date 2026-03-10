import os # To take the getenv function and navigate through the files
from sqlalchemy import create_engine # Creates database engine
from dotenv import load_dotenv # To take env var

load_dotenv()

def get_db_engine(): 
    db_url = os.getenv("DATABASE_URL") # Takes the database connection string
    if not db_url:
        raise ValueError("DATABASE_URL not found in .env file") # If it isn't there, raise an error
    
    return create_engine(db_url) # Else creates the database engine

def load_to_postgres(df, table_name="src_cars"): # df (from extract.py) and table name as parameters
    try:
        engine = get_db_engine() # Call the engine function
        df.to_sql(table_name, engine, if_exists='replace', index=False) # Passing the data through a sql normalizing
        print(f"Successfully loaded {len(df)} rows into {table_name}") # Printing how may cars are loaded and the table name
    except Exception as e:
        print(f"Error during Load: {e}") # Exception in case of failure