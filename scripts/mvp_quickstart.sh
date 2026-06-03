#!/bin/bash
# MVP Quickstart Script for K12 Knowledge Repository
# Spins up core services with minimal configuration for local testing

set -e

echo "========================================"
echo "K12 Knowledge Repository - MVP Quickstart"
echo "========================================"
echo ""

# Check prerequisites
echo "[1/6] Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi
echo "✓ Docker and Docker Compose found"

# Create .env file if it doesn't exist
echo ""
echo "[2/6] Setting up environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please review .env and update with your configurations"
else
    echo "✓ .env file exists"
fi

# Create necessary directories
echo ""
echo "[3/6] Creating data directories..."
mkdir -p data/milvus data/minio data/etcd data/sample
echo "✓ Directories created"

# Pull latest images
echo ""
echo "[4/6] Pulling Docker images (this may take a few minutes)..."
docker-compose pull
echo "✓ Images pulled"

# Start services
echo ""
echo "[5/6] Starting services..."
docker-compose up -d milvus etcd minio jaeger prometheus grafana
echo "✓ Infrastructure services started"

# Wait for services to be ready
echo ""
echo "[6/6] Waiting for services to be ready..."
sleep 10
echo "✓ Services should be ready"

# Display service status
echo ""
echo "========================================"
echo "MVP Services Status"
echo "========================================"
docker-compose ps

echo ""
echo "========================================"
echo "Service Endpoints:"
echo "========================================"
echo "Retrieval API:     http://localhost:8000"
echo "Agent API:         http://localhost:8001"
echo "Grafana:           http://localhost:3000 (admin/admin)"
echo "Jaeger UI:         http://localhost:16686"
echo "Prometheus:        http://localhost:9090"
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo "1. Start application services:"
echo "   docker-compose up -d retrieval agent"
echo ""
echo "2. Load sample data:"
echo "   python scripts/ingest_sources.py --sample"
echo ""
echo "3. Test retrieval:"
echo "   curl http://localhost:8000/health"
echo ""
echo "4. View telemetry:"
echo "   Open Grafana at http://localhost:3000"
echo ""
echo "5. Stop all services:"
echo "   docker-compose down"
echo "========================================"
echo ""
