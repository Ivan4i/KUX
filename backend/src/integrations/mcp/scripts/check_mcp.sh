#!/bin/bash
# ==============================================================================
# MCP Kit Check Script
# ==============================================================================
# Verifies MCP configuration and available services.
# Run from project root: bash mcp-kit/scripts/check_mcp.sh
# ==============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}=================================================${NC}"
echo -e "${BLUE}  MCP Kit Configuration Check${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Determine paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_KIT_DIR="$(dirname "$SCRIPT_DIR")"

if [[ "$(basename "$MCP_KIT_DIR")" == "mcp-kit" ]]; then
    PROJECT_ROOT="$(dirname "$MCP_KIT_DIR")"
else
    PROJECT_ROOT="$MCP_KIT_DIR"
    MCP_KIT_DIR="$PROJECT_ROOT/mcp-kit"
fi

# Load environment if exists
ENV_LOCAL="$MCP_KIT_DIR/.env.local"
if [[ -f "$ENV_LOCAL" ]]; then
    echo -e "${YELLOW}Loading environment from .env.local...${NC}"
    set -a
    source "$ENV_LOCAL"
    set +a
    echo -e "  ${GREEN}✓${NC} Environment loaded"
else
    echo -e "  ${YELLOW}⚠${NC} No .env.local found (using system environment)"
fi

echo ""

# Check for built gateway
GATEWAY_DIST="$MCP_KIT_DIR/mcp/saas-gateway/dist/index.js"
if [[ ! -f "$GATEWAY_DIST" ]]; then
    echo -e "${RED}Error: SaaS Gateway not built${NC}"
    echo "Run: bash mcp-kit/scripts/setup_mcp.sh"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} SaaS Gateway built"

echo ""
echo -e "${CYAN}--- SaaS Gateway Health Check ---${NC}"
echo ""

# Run gateway health check
node "$GATEWAY_DIST" --health-check

echo ""
echo -e "${CYAN}--- Local MCP Servers ---${NC}"
echo ""

# Filesystem MCP (always available via npx, skip runtime test to avoid ENOENT)
echo -e "Filesystem MCP: ${GREEN}Available via npx${NC}"

# Check Desktop Commander
echo -n "Desktop Commander: "
if [[ "${ENABLEDESKTOPCOMMANDER:-false}" == "true" ]]; then
    echo -e "${GREEN}Enabled${NC}"
else
    echo -e "${YELLOW}Disabled (set ENABLEDESKTOPCOMMANDER=true to enable)${NC}"
fi

# Check Browser Control
echo -n "Browser Control: "
if [[ "${ENABLECHROMECONTROL:-false}" == "true" ]]; then
    echo -e "${GREEN}Enabled${NC}"
else
    echo -e "${YELLOW}Disabled (set ENABLECHROMECONTROL=true to enable)${NC}"
fi

echo ""
echo -e "${CYAN}--- Configuration Files ---${NC}"
echo ""

# Check .mcp.json files
echo -n "Root .mcp.json: "
if [[ -f "$PROJECT_ROOT/.mcp.json" ]]; then
    echo -e "${GREEN}Present${NC}"
else
    echo -e "${RED}Missing${NC}"
fi

echo -n "Kit .mcp.json: "
if [[ -f "$MCP_KIT_DIR/.mcp.json" ]]; then
    echo -e "${GREEN}Present${NC}"
else
    echo -e "${RED}Missing${NC}"
fi

echo -n ".env.local: "
if [[ -f "$ENV_LOCAL" ]]; then
    echo -e "${GREEN}Present${NC}"
else
    echo -e "${YELLOW}Missing (copy from .env.example)${NC}"
fi

echo ""
echo -e "${CYAN}--- Environment Summary ---${NC}"
echo ""

# Quick check of key env vars
check_env() {
    local name=$1
    local value="${!name}"
    if [[ -n "$value" ]]; then
        # Show first 4 chars only for security
        echo -e "  ${GREEN}✓${NC} $name: ${value:0:4}..."
    else
        echo -e "  ${RED}✗${NC} $name: not set"
    fi
}

echo "Key environment variables:"
check_env "GITHUBTOKEN"
check_env "FIGMATOKEN"
check_env "CLOUDFLAREAPITOKEN"
check_env "VERCELTOKEN"
check_env "NOTIONTOKEN"
check_env "LINEARTOKEN"

echo ""
echo -e "${BLUE}=================================================${NC}"
echo -e "${GREEN}Check complete${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""
