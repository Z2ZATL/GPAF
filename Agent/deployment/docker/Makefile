.PHONY: help build run stop restart logs shell clean pull update

# Default target
help:
	@echo "Available commands:"
	@echo "  make build      - Build the Docker image"
	@echo "  make run        - Run the Docker container"
	@echo "  make stop       - Stop the Docker container"
	@echo "  make restart    - Restart the Docker container"
	@echo "  make logs       - View container logs"
	@echo "  make shell      - Open shell in container"
	@echo "  make clean      - Remove containers and images"
	@echo "  make pull       - Pull latest images"
	@echo "  make update     - Pull and restart containers"

# Build Docker image
build:
	docker-compose build

# Run containers
run:
	docker-compose up -d

# Run with Ollama
run-ollama:
	docker-compose --profile ollama up -d

# Stop containers
stop:
	docker-compose down

# Restart containers
restart:
	docker-compose restart

# View logs
logs:
	docker-compose logs -f

# Open shell in GPAF container
shell:
	docker exec -it gpaf /bin/bash

# Clean up
clean:
	docker-compose down -v
	docker rmi frdel/agent-zero-run:latest || true
	docker rmi gpaf:latest || true

# Pull latest images
pull:
	docker pull frdel/agent-zero-run:latest
	docker pull frdel/agent-zero-base:latest
	docker pull ollama/ollama:latest

# Update and restart
update: pull restart 