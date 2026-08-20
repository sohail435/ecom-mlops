# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies if required
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the gateway port (Render maps its own PORT environment variable)
EXPOSE 8000

# Command to run the API Gateway using Uvicorn
CMD ["uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "8000"]