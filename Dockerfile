# GPAF (General Purpose Agentic Framework) Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    wget \
    openssh-server \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Configure SSH (for code execution)
RUN mkdir -p /var/run/sshd
RUN echo 'root:gpaf123' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

# Copy requirements first for better Docker layer caching
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional production dependencies
RUN pip install --no-cache-dir gunicorn gevent supervisor

# Pre-download tiktoken encoding files to avoid runtime SSL issues
RUN python -c "import tiktoken; tiktoken.get_encoding('cl100k_base'); tiktoken.get_encoding('p50k_base'); tiktoken.get_encoding('r50k_base')" || echo "Warning: Failed to pre-download tiktoken encodings, will use fallback"

# Copy entire project
COPY . /app/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV TIKTOKEN_CACHE_DIR=/tmp/tiktoken_cache

# Create necessary directories
RUN mkdir -p /tmp/tiktoken_cache
RUN mkdir -p /app/memory
RUN mkdir -p /app/knowledge
RUN mkdir -p /app/logs
RUN mkdir -p /app/work_dir
RUN mkdir -p /app/tmp

# Create supervisor configuration
RUN cat > /etc/supervisor/conf.d/supervisord.conf << 'EOF'
[supervisord]
nodaemon=true
user=root

[program:sshd]
command=/usr/sbin/sshd -D
autostart=true
autorestart=true

[program:gpaf]
command=python run_ui.py
directory=/app
autostart=true
autorestart=true
stdout_logfile=/app/logs/gpaf.log
stderr_logfile=/app/logs/gpaf_error.log
environment=PYTHONPATH=/app,PYTHONUNBUFFERED=1
user=root
EOF

# Expose ports
EXPOSE 5000 22

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]