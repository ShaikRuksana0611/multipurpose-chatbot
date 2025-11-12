FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Create necessary directories
RUN mkdir -p backend/data backend/logs

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend.app:create_app()", "--workers", "4"]