import streamlit as st
import requests
import pandas as pd
import json 
# FastAPI endpoint
FASTAPI_URL = "http://app:8000/get_data_from_mongo"

# Function to fetch flight data
def get_flights():
    response = requests.get(FASTAPI_URL)
    return response.json()

def display_flights():
    st.title("Flight Information")
    
    # Add a button to fetch flight data
    if st.button("Fetch Flights"):
        flights = get_flights()

        # Convert data to DataFrame for better display in Streamlit
        if flights:
            
            flights = json.loads(flights)
            try:
                df = pd.DataFrame(flights)
                st.dataframe(df)
            except Exception as e:
                st.write(f"Error: {e}")
        else:
            st.write("No data available.")


if __name__ == "__main__":
    display_flights()
