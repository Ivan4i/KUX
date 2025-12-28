#!/bin/bash
# KUX Stop Script - Stop all services
# Usage: ./scripts/stop.sh

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}       KUX - MultiDevice Automation System      ${NC}"
echo -e "${BLUE}              Stopping Services...              ${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# PID files
BACKEND_PID_FILE="$PROJECT_ROOT/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.frontend.pid"

# Function to stop process
stop_process() {
    local name=$1
    local pid_file=$2
    local process_pattern=$3

    echo -e "${YELLOW}Stopping $name...${NC}"

    # Try to stop using PID file
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid 2>/dev/null
            echo -e "  ${GREEN}Stopped process $pid${NC}"
        fi
        rm -f "$pid_file"
    fi

    # Also kill by pattern (in case PID file is stale)
    if [ -n "$process_pattern" ]; then
        pkill -f "$process_pattern" 2>/dev/null || true
    fi
}

# Stop Backend (uvicorn)
stop_process "Backend" "$BACKEND_PID_FILE" "uvicorn src.main:app"

# Stop Frontend (Vite)
stop_process "Frontend" "$FRONTEND_PID_FILE" "vite"

# Additional cleanup - kill any remaining processes on ports
echo ""
echo -e "${YELLOW}Cleaning up ports...${NC}"

# Kill process on port 8000 (backend)
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    lsof -Pi :8000 -sTCP:LISTEN -t | xargs kill -9 2>/dev/null || true
    echo -e "  ${GREEN}Released port 8000${NC}"
fi

# Kill process on port 5173 (frontend)
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    lsof -Pi :5173 -sTCP:LISTEN -t | xargs kill -9 2>/dev/null || true
    echo -e "  ${GREEN}Released port 5173${NC}"
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}              Services Stopped!                  ${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "To start services again: ${BLUE}./scripts/start.sh${NC}"
echo ""
