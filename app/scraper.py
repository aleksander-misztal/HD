import requests
from bs4 import BeautifulSoup
import time
import random
from tenacity import retry, stop_after_attempt, wait_exponential
import json 
from pymongo import MongoClient
import os

class Scraper:
    def __init__(self) -> None:
        self.URL = 'https://www.jakdolece.pl/rozklad-lotow/warszawa-waw/odloty'
        self.html_file = 'schedule_data.html'
    
    def fetch_clean_and_save(self):
        # 1) Pozyskaj Surowe Dane
        data = self.retrieve_schedule_data()
        # # 2) Wyczysc Dane
        data = self.clean_data()
        # # 3) Zapisz Dane
        self.store_data(data = data)
        pass
    
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
    def retrieve_schedule_data(self):
        """
        Connects to the website URL and retrieves the raw HTML source code.
        Also prints out the response headers.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36',  # Updated to Chrome User-Agent
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        try:
            # Send GET request using requests Session to maintain cookies and headers
            with requests.Session() as session:
                session.headers.update(headers)
                response = session.get(self.URL)

                # Check if the request was successful (status code 200)
                response.raise_for_status()
                
                # Print response headers
                print("Response Headers:")
                for header, value in response.headers.items():
                    print(f"{header}: {value}")

                # Save the raw HTML content to a file
                with open(self.html_file, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                    print(f"HTML saved to {self.html_file}")

                # Return the raw HTML source code
                return response.text

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    

    def clean_data(self):
        # Otwórz plik HTML
        with open('schedule_data.html', 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parsowanie HTML za pomocą BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Znajdź wszystkie wiersze w tabeli
        rows = soup.find_all("tr")

        # Lista do przechowywania danych
        flights_list = []

        # Iteracja po wierszach (pomijamy reklamy)
        for row in rows:
            # Pomijamy wiersze z reklamami (mają klasę "ad")
            if 'ad' in row.get('class', []):
                continue

            # Szukamy wszystkich kolumn (td elements)
            cols = row.find_all("td")
            
            # Jeśli kolumny istnieją, przetwarzamy dane
            if cols:
                # Sprawdzamy, czy wiersz zawiera wystarczającą liczbę kolumn
                if len(cols) >= 5:  # Sprawdzamy, czy wiersz ma co najmniej 5 kolumn
                    # Bezpieczne pobieranie nagłówka "Czas"
                    czas_elem = row.find("th", {"data-label": "Czas"})
                    czas = czas_elem.text.strip() if czas_elem else None

                    # Bezpieczne pobieranie danych pozostałych komórek
                    kierunek = cols[0].text.strip()
                    nr_lotu = cols[1].text.strip()
                    linie = cols[2].find("img")["title"] if cols[2].find("img") else None
                    status = cols[3].text.strip()
                    uwagi = cols[4].text.strip()

                    # Tworzymy słownik z danymi lotu
                    flight_data = {
                        "Czas": czas,
                        "Kierunek": kierunek,
                        "Nr lotu": nr_lotu,
                        "Linie": linie,
                        "Status": status,
                        "Uwagi": uwagi
                    }
                    flights_list.append(flight_data)
                    
        # Function to clean dictionaries by removing fields with None or '-'
        def clean_flights(flights):
            cleaned_flights = []
            for flight in flights:
                cleaned_flight = {key: value for key, value in flight.items() if value not in [None, '-']}
                cleaned_flights.append(cleaned_flight)
            return cleaned_flights

        # Clean the list of flights
        cleaned_flights = clean_flights(flights_list)
        print(clean_flights)
        

        return cleaned_flights

    
    def store_data(self, data):
        # Fetch MongoDB connection details from environment variables
        mongo_uri = os.getenv("MONGO_URI")

        # Check if the environment variable is set
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set!")

        try:
            # Connect to MongoDB without authentication (using the provided URI)
            print("Connecting to MongoDB using URI:", mongo_uri)
            client = MongoClient(mongo_uri)

            # Access the database and collection
            db = client["flights_db"]  # Using the database "flights_db"
            collection = db["WarsawDepartures"]  # Using the "WarsawDepartures" collection

            # Insert the list of JSON objects into the collection
            result = collection.insert_many(data)

            # Output the result (e.g., IDs of inserted documents)
            print(f"Inserted {len(result.inserted_ids)} records into 'WarsawDepartures' collection.")

        except Exception as e:
            # Handle any connection or operation errors
            print(f"An error occurred while interacting with MongoDB: {e}")
        finally:
            # Ensure that the connection is always closed
            if 'client' in locals():
                client.close()
                print("MongoDB connection closed.")
    

    
    