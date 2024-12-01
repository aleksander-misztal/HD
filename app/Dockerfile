# Używamy oficjalnego obrazu Python 3.11 jako bazowego
FROM python:3.11-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR .

# Kopiujemy plik requirements.txt do kontenera
COPY requirements.txt .

# Instalujemy zależności z pliku requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy cały kod aplikacji do kontenera
COPY . .

# Sprawdzamy, czy uvicorn jest poprawnie zainstalowany
RUN pip show uvicorn

# Ustawiamy domyślny port
EXPOSE 8000

# Uruchamiamy aplikację FastAPI za pomocą Uvicorn
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
