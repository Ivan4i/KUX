#!/bin/bash
# ==============================================================================
# VS Code Launcher for Claude Code Account 4
# ==============================================================================
# Launches VS Code with isolated user-data and extensions directories.
# Each account gets its own Claude Code session and environment.
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_KIT_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$MCP_KIT_DIR")"

# Load environment for this account
ENV_FILE="$MCP_KIT_DIR/.env.local.acc4"
if [[ -f "$ENV_FILE" ]]; then
    echo "Loading environment from: $ENV_FILE"
    set -a && source "$ENV_FILE" && set +a
else
    echo "Warning: $ENV_FILE not found, using default .env.local"
    set -a && source "$MCP_KIT_DIR/.env.local" && set +a
fi

# Launch VS Code with isolated directories
cd "$PROJECT_ROOT"
code . --user-data-dir ~/.vscode-claude/acc4 --extensions-dir ~/.vscode-claude/acc4-exts
