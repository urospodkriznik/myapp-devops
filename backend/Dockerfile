FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app ./app
COPY alembic.ini .
COPY ./alembic ./alembic

# Install system dependencies (for CloudSQL / psycopg / pg client)
RUN apt-get update && apt-get install -y \
    postgresql-client libpq-dev gcc libc-dev libnss-wrapper libpam0g \
    && rm -rf /var/lib/apt/lists/*

# Create CloudSQL socket dir (for /cloudsql path)
RUN mkdir -p /cloudsql

# Expose port Cloud Run expects
EXPOSE 8080

# Start Uvicorn on port 8080 (what Cloud Run expects)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]