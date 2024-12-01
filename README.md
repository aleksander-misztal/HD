
# **Flight Data Scraper API with Streamlit**

This project provides a comprehensive system for scraping, storing, and visualizing flight departure data from Warsaw. It uses **FastAPI** for backend services, **MongoDB** for data storage, and **Streamlit** for a user-friendly frontend.

---

## **Features**

- **FastAPI Endpoints**:
  - Scrape, clean, and store flight departure data in MongoDB.
  - Retrieve stored data from MongoDB.
  - Upload CSV files and load them into MongoDB.
  - Delete all records from the MongoDB collection.

- **Streamlit Interface**:
  - Fetch and display flight data interactively.
  - Visualize data in a tabular format.

- **Docker Compose**:
  - Simplifies deployment with a pre-configured stack including API, database, and frontend.

---

## **Architecture**

The application consists of three main services:
1. **app**: Backend (FastAPI) for data scraping, cleaning, and MongoDB interactions.
2. **mongo**: MongoDB for storing flight and CSV data.
3. **streamlit**: Frontend (Streamlit) for visualizing the stored data.

---

## **Setup Instructions**

### **Prerequisites**
- Docker and Docker Compose
- MongoDB URI (set as an environment variable in the `docker-compose.yml` file)

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flight-data-scraper.git
   cd flight-data-scraper
   ```

2. Build and start services using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - **FastAPI Backend**: [http://localhost:8000](http://localhost:8000)
   - **Streamlit Frontend**: [http://localhost:8501](http://localhost:8501)
   - **MongoDB**: [http://localhost:28017](http://localhost:28017)

4. Stop all services:
   ```bash
   docker-compose down
   ```

---

## **API Endpoints**

### **1. `/retrieve_departure_data`**
**Method**: `GET`  
**Description**: Scrapes flight departure data, cleans it, and saves it to MongoDB.

**Response**:
- `200 OK`: Data successfully retrieved and saved.
- `500 Internal Server Error`: An error occurred during scraping or saving.

---

### **2. `/get_data_from_mongo`**
**Method**: `GET`  
**Description**: Retrieves all flight departure data stored in MongoDB.

**Response**:
- `200 OK`: Returns a JSON array of flight data.
- `500 Internal Server Error`: An error occurred with MongoDB.

---

### **3. `/delete_all_rows`**
**Method**: `DELETE`  
**Description**: Deletes all records from the `WarsawDepartures` collection in MongoDB.

**Response**:
- `200 OK`: Returns the number of deleted records.
- `500 Internal Server Error`: An error occurred while interacting with MongoDB.

---

### **4. `/load_csv`**
**Method**: `POST`  
**Description**: Uploads a CSV file and stores its content in the `csv_data` collection in MongoDB.

**Request**:
- **File**: A CSV file.

**Response**:
- `200 OK`: Number of records successfully inserted into the collection.
- `400 Bad Request`: The uploaded file is not a CSV.
- `500 Internal Server Error`: An error occurred while processing the file.

---

## **Streamlit Frontend**

- Navigate to [http://localhost:8501](http://localhost:8501).
- Features:
  - **Fetch Flights**: A button to dynamically fetch flight data from the API and display it in a table.
  - **Data Table**: Displays flight data in a structured and readable format using **pandas**.

---

## **MongoDB Configuration**

- **Database**: `flights_db`
- **Collections**:
  - `WarsawDepartures`: Stores scraped flight departure data.
  - `csv_data`: Stores uploaded CSV data.

- Connection details:
  - Defined in the `docker-compose.yml` file as `mongodb://mongo:27017/`.

---

## **Docker Compose**

The `docker-compose.yml` orchestrates the three services:
1. **app**: Runs the FastAPI backend on port `8000`.
2. **mongo**: Runs a MongoDB instance on port `27017`.
3. **streamlit**: Runs the Streamlit frontend on port `8501`.

**Workflow**:
- Start all services:
  ```bash
  docker-compose up --build
  ```
- Stop all services:
  ```bash
  docker-compose down
  ```

---

## **Technologies Used**

- **FastAPI**: Backend API for data scraping and management.
- **MongoDB**: Database for storing flight and CSV data.
- **Streamlit**: Frontend for visualizing flight data.
- **BeautifulSoup**: HTML parsing for data scraping.
- **pandas**: Data manipulation for table displays.
- **tenacity**: Retry mechanism for failed scraping requests.
- **Docker**: Containerization and deployment.

---
