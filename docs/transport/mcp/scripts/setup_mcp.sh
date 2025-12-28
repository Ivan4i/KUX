#!/bin/bash
# ==============================================================================
# MCP Kit Setup Script
# ==============================================================================
# This script sets up the MCP infrastructure for Claude Code.
# Run from project root: bash mcp-kit/scripts/setup_mcp.sh
# Or from mcp-kit folder: bash scripts/setup_mcp.sh
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================================${NC}"
echo -e "${BLUE}  MCP Kit Setup${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Determine script location and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_KIT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if we're in mcp-kit or project root
if [[ "$(basename "$MCP_KIT_DIR")" == "mcp-kit" ]]; then
    PROJECT_ROOT="$(dirname "$MCP_KIT_DIR")"
else
    # Assume script is run from project root with mcp-kit subfolder
    PROJECT_ROOT="$MCP_KIT_DIR"
    MCP_KIT_DIR="$PROJECT_ROOT/mcp-kit"
fi

echo -e "Project root: ${GREEN}$PROJECT_ROOT${NC}"
echo -e "MCP Kit dir:  ${GREEN}$MCP_KIT_DIR${NC}"
echo ""

# Check for required tools
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [[ "$NODE_VERSION" -lt 18 ]]; then
    echo -e "${RED}Error: Node.js 18+ required (found v$NODE_VERSION)${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Node.js $(node -v)"

if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} npm $(npm -v)"

echo ""

# Create .env.local if it doesn't exist
ENV_EXAMPLE="$MCP_KIT_DIR/.env.example"
ENV_LOCAL="$MCP_KIT_DIR/.env.local"

if [[ ! -f "$ENV_LOCAL" ]]; then
    echo -e "${YELLOW}Creating .env.local from template...${NC}"
    cp "$ENV_EXAMPLE" "$ENV_LOCAL"
    echo -e "  ${GREEN}✓${NC} Created $ENV_LOCAL"
else
    echo -e "  ${GREEN}✓${NC} .env.local already exists"
fi

echo ""

# Install dependencies for saas-gateway
GATEWAY_DIR="$MCP_KIT_DIR/mcp/saas-gateway"
echo -e "${YELLOW}Installing saas-gateway dependencies...${NC}"
cd "$GATEWAY_DIR"
npm install
echo -e "  ${GREEN}✓${NC} Dependencies installed"

echo ""

# Build saas-gateway
echo -e "${YELLOW}Building saas-gateway...${NC}"
npm run build
echo -e "  ${GREEN}✓${NC} Build complete"

echo ""

# Copy/update root .mcp.json if needed
ROOT_MCP="$PROJECT_ROOT/.mcp.json"
KIT_MCP="$MCP_KIT_DIR/.mcp.json"

if [[ ! -f "$ROOT_MCP" ]] || [[ "$KIT_MCP" -nt "$ROOT_MCP" ]]; then
    echo -e "${YELLOW}Updating root .mcp.json...${NC}"
    cp "$KIT_MCP" "$ROOT_MCP"
    echo -e "  ${GREEN}✓${NC} Root .mcp.json updated"
else
    echo -e "  ${GREEN}✓${NC} Root .mcp.json is up to date"
fi

echo ""

# Create .sandbox directory if needed
SANDBOX_DIR="$PROJECT_ROOT/.sandbox"
if [[ ! -d "$SANDBOX_DIR" ]]; then
    mkdir -p "$SANDBOX_DIR"
    echo -e "  ${GREEN}✓${NC} Created .sandbox directory"
fi

echo ""
echo -e "${BLUE}=================================================${NC}"
echo -e "${GREEN}Setup complete!${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "1. Edit your tokens in:"
echo -e "   ${GREEN}$ENV_LOCAL${NC}"
echo ""
echo "2. At minimum, fill in tokens for services you need:"
echo "   - GITHUB_TOKEN (GitHub API)"
echo "   - FIGMA_TOKEN (Figma API)"
echo "   - CLOUDFLARE_API_TOKEN (Cloudflare API)"
echo "   - etc."
echo ""
echo "3. Open VS Code from terminal to load environment:"
echo -e "   ${GREEN}source $ENV_LOCAL && code .${NC}"
echo ""
echo "4. Or check configuration:"
echo -e "   ${GREEN}bash mcp-kit/scripts/check_mcp.sh${NC}"
echo ""
echo "5. Optional: Enable Desktop Commander or Chrome Control:"
echo "   ENABLE_DESKTOP_COMMANDER=true"
echo "   ENABLE_CHROME_CONTROL=true"
echo ""
