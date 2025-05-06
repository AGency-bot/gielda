# Używamy oficjalnego obrazu Pythona
FROM python:3.11-slim

# Katalog roboczy
WORKDIR /app

# Kopiujemy zależności
COPY requirements.txt .

# Instalacja
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę kodu
COPY . .

# Uruchomienie serwera webhook (FastAPI)
CMD ["uvicorn", "webhook_server:app", "--host", "0.0.0.0", "--port", "8000"]
