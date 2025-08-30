#!/bin/bash

# GPAF Docker Build Script

set -e

echo "🐳 Building GPAF Docker Container..."

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down --remove-orphans 2>/dev/null || true
docker container rm gpaf_agent 2>/dev/null || true

# Build the container
echo "🔨 Building Docker image..."
docker-compose build --no-cache

echo "✅ Docker build completed!"
echo ""
echo "📋 Next steps:"
echo "1. Set your API keys in environment variables or create a .env file:"
echo "   export API_KEY_OPENAI='your-openai-key'"
echo "   export API_KEY_ANTHROPIC='your-anthropic-key'"
echo ""
echo "2. Start the container:"
echo "   docker-compose up -d"
echo ""
echo "3. Access GPAF:"
echo "   Web UI: http://localhost:50001"
echo "   Login: admin / gpaf123"
echo "   SSH: ssh -p 55022 root@localhost (password: gpaf123)"
echo ""
echo "4. View logs:"
echo "   docker-compose logs -f gpaf"
echo ""
echo "5. Stop the container:"
echo "   docker-compose down"