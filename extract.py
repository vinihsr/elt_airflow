import os # to get the env var
import pandas as pd # To treat the data
import requests as req # To use the HTTP methods and take the data from URL
from dotenv import load_dotenv # To use load dotenv here

load_dotenv() # Calling the dotenv to be accessed from here

def extract_car_data(): # Defining the extract function to be used on main

    api_key = os.getenv("API_KEY") # Api key from .env
    url = f"http://host.docker.internal/api/admin/cars?apikey={api_key}" # Seting the url to take cars data
    
    try:
        response = req.get(url) # Get method to take all content to response variable
        response.raise_for_status() # To raise error for 4?? and 5?? types of errors
        
        json_payload = response.json() # Passing the response to json format 
        raw_list = json_payload.get('data', []) # Creating a filter that separate the metadata from useful data
        
        df = pd.json_normalize(raw_list) # Normalizing it to avoid possible errors
        
        df['source_system'] = json_payload.get('source') # Adding source_system as a column,  
        df['extraction_timestamp'] = json_payload.get('timestamp') # Adding times_tamp as a column
        
        print(f"Extraction successful: {len(df)} records found.") # Printing the cars counted
        return df # Returning all the data

    except Exception as e: # Creating an exception for cars that was not found
        print(f"Extraction failed: {e}") 
        return None 
