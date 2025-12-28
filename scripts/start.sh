#!/bin/bash
# KUX Start Script - Start all services
# Usage: ./scripts/start.sh [--backend-only] [--frontend-only]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Parse arguments
BACKEND_ONLY=0
FRONTEND_ONLY=0

for arg in "$@"; do
    case $arg in
        --backend-only)
            BACKEND_ONLY=1
            shift
            ;;
        --frontend-only)
            FRONTEND_ONLY=1
            shift
            ;;
    esac
done

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}       KUX - MultiDevice Automation System      ${NC}"
echo -e "${BLUE}              Starting Services...              ${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# PID files
BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.frontend.pid"

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port in use
    fi
    return 1  # Port free
}

# Function to wait for service
wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=1

    echo -n "  Waiting for $name..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e " ${GREEN}Ready!${NC}"
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
        echo -n "."
    done
    echo -e " ${RED}Timeout${NC}"
    return 1
}

# Start Backend
start_backend() {
    echo -e "${YELLOW}Starting Backend...${NC}"

    if check_port 8000; then
        echo -e "${YELLOW}  Port 8000 already in use. Backend may already be running.${NC}"
        return 0
    fi

    cd "$PROJECT_ROOT/backend"

    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        echo -e "${RED}  Virtual environment not found. Run ./scripts/setup.sh first.${NC}"
        return 1
    fi

    # Start uvicorn in background
    nohup python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload > "$PROJECT_ROOT/data/logs/backend.log" 2>&1 &
    echo $! > "$BACKEND_PID_FILE"

    wait_for_service "http://localhost:8000/health" "Backend"

    echo -e "${GREEN}  Backend started on http://localhost:8000${NC}"
}

# Start Frontend
start_frontend() {
    echo -e "${YELLOW}Starting Frontend...${NC}"

    if check_port 5173; then
        echo -e "${YELLOW}  Port 5173 already in use. Frontend may already be running.${NC}"
        return 0
    fi

    cd "$PROJECT_ROOT/frontend"

    # Start Vite dev server in background
    nohup npm run dev > "$PROJECT_ROOT/data/logs/frontend.log" 2>&1 &
    echo $! > "$FRONTEND_PID_FILE"

    wait_for_service "http://localhost:5173" "Frontend"

    echo -e "${GREEN}  Frontend started on http://localhost:5173${NC}"
}

# Create logs directory
mkdir -p "$PROJECT_ROOT/data/logs"

# Start services based on arguments
if [ $FRONTEND_ONLY -eq 1 ]; then
    start_frontend
elif [ $BACKEND_ONLY -eq 1 ]; then
    start_backend
else
    start_backend
    echo ""
    start_frontend
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}              Services Started!                  ${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "Access the application:"
echo -e "  - Frontend:  ${BLUE}http://localhost:5173${NC}"
echo -e "  - Backend:   ${BLUE}http://localhost:8000${NC}"
echo -e "  - API Docs:  ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "Logs:"
echo -e "  - Backend:   ${BLUE}data/logs/backend.log${NC}"
echo -e "  - Frontend:  ${BLUE}data/logs/frontend.log${NC}"
echo ""
echo -e "To stop services: ${BLUE}./scripts/stop.sh${NC}"
echo ""
