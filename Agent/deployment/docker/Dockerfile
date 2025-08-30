# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY config/requirements.txt /app/config/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r config/requirements.txt

# Install additional production dependencies
RUN pip install --no-cache-dir gunicorn gevent

# Pre-download tiktoken encoding files to avoid runtime SSL issues
RUN python -c "import tiktoken; tiktoken.get_encoding('cl100k_base'); tiktoken.get_encoding('p50k_base'); tiktoken.get_encoding('r50k_base')" || echo "Warning: Failed to pre-download tiktoken encodings, will use fallback"

# Copy entire project
COPY . /app/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV TIKTOKEN_CACHE_DIR=/tmp/tiktoken_cache

# Create tiktoken cache directory
RUN mkdir -p /tmp/tiktoken_cache

# Expose port
EXPOSE 5000

# Run with gunicorn for production using config file
CMD ["gunicorn", "--config", "config/gunicorn.conf.py", "scripts.run_ui:app"] 