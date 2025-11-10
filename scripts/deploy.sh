#!/bin/bash
# Deploy script for powermem

set -e

echo "Deploying powermem..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed"
    exit 1
fi

# Build Docker image
echo "Building Docker image..."
docker build -t powermem:latest .

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down

# Start new containers
echo "Starting new containers..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Check health
echo "Checking service health..."
curl -f http://localhost:8000/api/v1/health || {
    echo "Error: Service health check failed"
    exit 1
}

echo "Deployment completed successfully!"
echo "Service is available at http://localhost:8000"
