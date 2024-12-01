
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pymongo import MongoClient, errors
from scraper import Scraper
import traceback
import json
import os
import pandas as pd
app = FastAPI()

mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise ValueError("MONGO_URI environment variable is not set!")

client = MongoClient(mongo_uri)
db = client["flights_db"]
collection = db["WarsawDepartures"]

@app.get("/retrieve_departure_data")
def retrieve_departure_data():
    try:
        scraper = Scraper()
        scraper.fetch_clean_and_save()
        return {"message": "Data successfully retrieved and saved."}
    
    except Exception as e:
        error_message = str(e)
        traceback_message = traceback.format_exc()  
        
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {error_message}",
            headers={"X-Error": traceback_message}  
        )

@app.get("/get_data_from_mongo")
def get_data_from_mongo():
    try:
        rows = collection.find()
        rows_list = list(rows)

        rows_list = [{k: v for k, v in d.items() if k != list(d.keys())[0]} for d in rows_list]

        json_data = json.dumps(rows_list)
        
        return JSONResponse(content=json_data)

    except errors.ConnectionError:
        raise HTTPException(status_code=500, detail="MongoDB connection failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete_all_rows")
async def delete_all_rows():
    # Pobranie URI MongoDB z zmiennych środowiskowych
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise HTTPException(status_code=500, detail="MONGO_URI environment variable is not set!")

    try:
        # Połączenie z MongoDB
        print("Connecting to MongoDB using URI:", mongo_uri)
        client = MongoClient(mongo_uri)

        # Dostęp do bazy i kolekcji
        db = client["flights_db"]
        collection = db["WarsawDepartures"]

        # Usuwanie wszystkich dokumentów
        result = collection.delete_many({})  # Usuwa wszystkie dokumenty
        print(f"Deleted {result.deleted_count} records from 'WarsawDepartures' collection.")

        return {
            "message": "All records deleted successfully.",
            "deleted_count": result.deleted_count
        }

    except Exception as e:
        # Obsługa błędów
        print(f"An error occurred while interacting with MongoDB: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Zamknięcie połączenia z MongoDB
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")
            
@app.post("/load_csv")
async def load_csv(file: UploadFile):
    # Pobranie URI MongoDB z zmiennych środowiskowych
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise HTTPException(status_code=500, detail="MONGO_URI environment variable is not set!")

    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        # Połączenie z MongoDB
        print("Connecting to MongoDB using URI:", mongo_uri)
        client = MongoClient(mongo_uri)

        # Dostęp do bazy i kolekcji
        db = client["flights_db"]
        collection = db["csv_data"]

        # Wczytanie pliku CSV jako DataFrame Pandas
        df = pd.read_csv(file.file)

        # Konwersja DataFrame do listy dokumentów JSON
        data = df.to_dict(orient="records")

        # Wstawianie danych do kolekcji
        result = collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} records into 'csv_data' collection.")

        return {
            "message": "Data successfully loaded from CSV.",
            "inserted_count": len(result.inserted_ids)
        }

    except Exception as e:
        # Obsługa błędów
        print(f"An error occurred while processing the CSV file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Zamknięcie połączenia z MongoDB
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")