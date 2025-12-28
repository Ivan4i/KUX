# MCP Kit - Model Context Protocol

**Location:** `tools/mcp/`
**Type:** Standalone Node.js/TypeScript service

---

## Overview

MCP (Model Context Protocol) enables AI agents to interact with external SaaS services. This kit provides pre-configured connectors for 13 services.

---

## Documentation Files

| File | Location |
|------|----------|
| README | `tools/mcp/README.md` |
| Detailed Docs | `tools/mcp/README_MCP.md` |

---

## Supported Services

| Service | Purpose |
|---------|---------|
| Cloudflare | CDN, DNS, Workers |
| Cloudinary | Image/video management |
| Figma | Design file access |
| GitHub | Repository operations |
| Linear | Issue tracking |
| MongoDB | Database operations |
| Monitoring | Health checks |
| Notion | Workspace integration |
| Postman | API testing |
| Sentry | Error monitoring |
| Supabase | Backend-as-a-Service |
| Vercel | Deployment platform |

---

## Directory Structure

```
tools/mcp/
├── config/
│   ├── mcp.json.example
│   └── .env.example
├── scripts/
│   ├── setup_mcp.sh
│   └── check_mcp.sh
├── secrets/                 # Credentials (gitignored)
├── src/
│   ├── index.ts
│   ├── services/           # Service connectors
│   └── utils/              # Utility functions
├── package.json
└── tsconfig.json
```

---

## Setup

```bash
cd tools/mcp

# 1. Install dependencies
npm install

# 2. Configure
cp config/.env.example config/.env
# Edit config/.env with your tokens

# 3. Build
npm run build

# 4. Test
npm run check
```

---

## Usage with Claude Code

Add to `.mcp.json` in project root:

```json
{
  "mcpServers": {
    "saas-gateway": {
      "command": "node",
      "args": ["tools/mcp/dist/index.js"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}",
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

---

## See Also

- Detailed setup: `tools/mcp/README_MCP.md`
- MCP Protocol: https://modelcontextprotocol.io/
