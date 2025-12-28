#!/bin/bash
# ==============================================================================
# MCP Config Link Script
# ==============================================================================
# Copies the .mcp.json from mcp-kit to project root.
# Useful after updates to mcp-kit/.mcp.json
# ==============================================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Determine paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_KIT_DIR="$(dirname "$SCRIPT_DIR")"

if [[ "$(basename "$MCP_KIT_DIR")" == "mcp-kit" ]]; then
    PROJECT_ROOT="$(dirname "$MCP_KIT_DIR")"
else
    PROJECT_ROOT="$MCP_KIT_DIR"
    MCP_KIT_DIR="$PROJECT_ROOT/mcp-kit"
fi

KIT_MCP="$MCP_KIT_DIR/.mcp.json"
ROOT_MCP="$PROJECT_ROOT/.mcp.json"

if [[ ! -f "$KIT_MCP" ]]; then
    echo "Error: $KIT_MCP not found"
    exit 1
fi

echo -e "${YELLOW}Copying .mcp.json to project root...${NC}"
cp "$KIT_MCP" "$ROOT_MCP"
echo -e "${GREEN}Done!${NC}"
echo ""
echo "Root .mcp.json has been updated from mcp-kit/.mcp.json"
