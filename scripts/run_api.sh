#!/bin/bash
# Run the FastAPI backend

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Run FastAPI with uvicorn
echo "Starting Water Risk Platform API..."
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo ""

uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
