# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run migrations, create sample data if needed, and start Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py populate_inventory && python manage.py runserver 0.0.0.0:8000"]
