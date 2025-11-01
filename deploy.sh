#!/bin/bash

# InsightScope Deployment Script
set -e

echo "🚀 Starting InsightScope deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from production template..."
    cp .env.production .env
    echo "⚠️  Please edit .env file with your configuration before running the application."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p vector_db data/processed data/raw

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting InsightScope application..."
docker-compose up -d

# Wait for the application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "✅ InsightScope is running successfully!"
    echo "🌐 Access the application at: http://localhost:8501"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo "📋 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop application: docker-compose down"
echo "  - Restart application: docker-compose restart"
echo "  - Update application: docker-compose pull && docker-compose up -d"