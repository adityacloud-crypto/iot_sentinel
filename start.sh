#!/bin/bash
# IoT Sentinel Startup Script for Render
# This script initializes the application and starts the API server

set -e

echo "🛡️  IoT Sentinel - Starting up..."

# Set default PORT if not specified
PORT=${PORT:-10000}
HOST=${HOST:-0.0.0.0}

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/raw data/processed data/uploads models static

# Check if model exists, if not create a dummy one for demo
if [ ! -f "models/isolation_forest.pkl" ]; then
    echo "⚠️  Model not found. Running in demo mode..."
    echo "💡 For production, upload trained model files to models/"
fi

# Check if processed data exists
if [ ! -f "data/processed/iot23_processed.csv" ]; then
    echo "ℹ️  No processed dataset found. API will run in demo mode."
    echo "💡 Upload IoT-23 dataset or use the /api/batch-score endpoint for demo data"
fi

# Install dependencies if needed (Render does this automatically)
if [ "$RENDER" != "true" ]; then
    echo "📦 Checking dependencies..."
    pip install -q -r requirements.txt 2>/dev/null || true
fi

# Start the API server
echo "🚀 Starting IoT Sentinel API server on $HOST:$PORT..."
echo "📊 Dashboard available at: http://localhost:$PORT/"
echo "📚 API docs available at: http://localhost:$PORT/api/docs"
echo ""
echo "═══════════════════════════════════════════════════"
echo "  IoT Sentinel - Enterprise IoT Anomaly Detection"
echo "  Powered by Isolation Forest ML"
echo "═══════════════════════════════════════════════════"
echo ""

# Run uvicorn
exec uvicorn src.api_server:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers 1 \
    --log-level info \
    --access-log
