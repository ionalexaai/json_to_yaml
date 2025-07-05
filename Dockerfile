# Use slim official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (optional, e.g., for compilation needs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (separate from requirements to leverage Docker cache)
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn, referencing app factory
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:5000", "--timeout", "90", "--access-logfile", "-"]

