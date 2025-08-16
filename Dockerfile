# Use official Python slim image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Make sure our app package is discoverable
ENV PYTHONPATH=/app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
