#!/bin/bash
# KUX Setup Script - One-command installation
# Usage: ./scripts/setup.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}       KUX - MultiDevice Automation System      ${NC}"
echo -e "${BLUE}                  Setup Script                  ${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Function to check command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        return 1
    fi
    return 0
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

MISSING=0

if ! check_command python3; then
    echo -e "${RED}  - Python 3 not found. Please install Python 3.11+${NC}"
    MISSING=1
fi

if ! check_command node; then
    echo -e "${RED}  - Node.js not found. Please install Node.js 18+${NC}"
    MISSING=1
fi

if ! check_command npm; then
    echo -e "${RED}  - npm not found. Please install npm${NC}"
    MISSING=1
fi

if [ $MISSING -eq 1 ]; then
    echo -e "${RED}Please install missing prerequisites and run again.${NC}"
    exit 1
fi

echo -e "${GREEN}All prerequisites found!${NC}"
echo ""

# Python version check
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${BLUE}Python version: ${PYTHON_VERSION}${NC}"

# Node version check
NODE_VERSION=$(node -v)
echo -e "${BLUE}Node.js version: ${NODE_VERSION}${NC}"
echo ""

# Setup Backend
echo -e "${YELLOW}Setting up Backend...${NC}"
cd "$PROJECT_ROOT/backend"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "  Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "  Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Copy .env.example to .env if not exists
if [ ! -f ".env" ]; then
    echo "  Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}  Please edit backend/.env with your API keys!${NC}"
fi

# Create data directories
mkdir -p data/screenshots
mkdir -p data/context
mkdir -p data/logs

echo -e "${GREEN}Backend setup complete!${NC}"
echo ""

# Setup Frontend
echo -e "${YELLOW}Setting up Frontend...${NC}"
cd "$PROJECT_ROOT/frontend"

# Install Node dependencies
echo "  Installing Node.js dependencies..."
npm install --silent

echo -e "${GREEN}Frontend setup complete!${NC}"
echo ""

# Initialize Database
echo -e "${YELLOW}Initializing Database...${NC}"
cd "$PROJECT_ROOT/backend"
source venv/bin/activate

# Run database initialization
python3 -c "
from src.database.db import init_db
import asyncio
asyncio.run(init_db())
print('Database initialized successfully!')
" 2>/dev/null || echo -e "${YELLOW}Database initialization skipped (may already exist)${NC}"

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}            Setup Complete!                      ${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "Next steps:"
echo -e "  1. Edit ${BLUE}backend/.env${NC} with your API keys"
echo -e "  2. Run ${BLUE}./scripts/start.sh${NC} to start services"
echo ""
echo -e "Configuration files:"
echo -e "  - Backend: ${BLUE}backend/.env${NC}"
echo -e "  - Devices: ${BLUE}config/devices.yaml${NC}"
echo ""
