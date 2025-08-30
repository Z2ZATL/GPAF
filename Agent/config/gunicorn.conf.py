#!/usr/bin/env python3
"""
Gunicorn Configuration for GPAF Production
"""

import os
import multiprocessing

# Server Socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker Processes
workers = 1  # GPAF ควรใช้ worker เดียวเพื่อหลีกเลี่ยงปัญหา shared state
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 30

# Application
pythonpath = "/app"
chdir = "/app"

# Logging
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
accesslog = "-"  # stdout
errorlog = "-"   # stderr

# Process Naming
proc_name = "gpaf-server"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# SSL (if needed)
# keyfile = None
# certfile = None

# Development vs Production
if os.getenv("FLASK_ENV") == "development":
    reload = True
    loglevel = "debug"
else:
    reload = False
    preload_app = True

# Environment Variables
raw_env = [
    f"TZ={os.getenv('TZ', 'UTC')}",
    f"PYTHONPATH={os.getenv('PYTHONPATH', '/app')}",
    f"DISABLE_RFC={os.getenv('DISABLE_RFC', 'true')}",
]

def when_ready(server):
    server.log.info("🚀 GPAF Server ready to serve requests!")

def worker_int(worker):
    worker.log.info("🔧 Worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info(f"🏗️ Worker spawned (pid: {worker.pid})")

def post_fork(server, worker):
    server.log.info(f"✅ Worker initialization complete (pid: {worker.pid})")

def worker_abort(worker):
    worker.log.info(f"❌ Worker received SIGABRT signal (pid: {worker.pid})") 