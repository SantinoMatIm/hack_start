#!/bin/bash
# Run the Streamlit dashboard

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Run Streamlit
echo "Starting Water Risk Platform Dashboard..."
echo "Dashboard: http://localhost:8501"
echo "Make sure the API server is running on http://localhost:8000"
echo ""

streamlit run dashboard/app.py --server.port 8501 --server.address localhost
