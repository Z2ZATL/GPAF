#!/bin/bash
# GPAF Docker Convenience Script

DOCKER_DIR="deployment/docker"

case "$1" in
    "build")
        echo "Building GPAF Docker image..."
        docker-compose -f $DOCKER_DIR/docker-compose.yml build
        ;;
    "up"|"start")
        echo "Starting GPAF container..."
        docker-compose -f $DOCKER_DIR/docker-compose.yml up -d
        ;;
    "down"|"stop")
        echo "Stopping GPAF container..."
        docker-compose -f $DOCKER_DIR/docker-compose.yml down
        ;;
    "restart")
        echo "Restarting GPAF container..."
        docker-compose -f $DOCKER_DIR/docker-compose.yml restart
        ;;
    "logs")
        echo "Showing GPAF logs..."
        docker-compose -f $DOCKER_DIR/docker-compose.yml logs -f
        ;;
    "shell")
        echo "Opening shell in GPAF container..."
        docker exec -it gpaf /bin/bash
        ;;
    "status")
        echo "Showing container status..."
        docker ps
        ;;
    *)
        echo "GPAF Docker Commands:"
        echo "  ./docker.sh build    - Build Docker image"
        echo "  ./docker.sh up       - Start container"
        echo "  ./docker.sh down     - Stop container" 
        echo "  ./docker.sh restart  - Restart container"
        echo "  ./docker.sh logs     - Show logs"
        echo "  ./docker.sh shell    - Open shell"
        echo "  ./docker.sh status   - Show status"
        echo ""
        echo "Or use: make -C $DOCKER_DIR [command]"
        ;;
esac 