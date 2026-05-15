# ================================
# Production Dockerfile for Render
# ================================
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer cache optimization)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Create logs directory (required by settings.py)
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Production: migrate + populate + gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py populate_inventory && gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120"]