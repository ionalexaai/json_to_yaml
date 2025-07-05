# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask default port
EXPOSE 5000

# Run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
