# MCP Kit - Model Context Protocol Integration

**Version:** 1.0.0
**Purpose:** Unified gateway for SaaS service integration with Claude/AI agents

---

## Overview

MCP (Model Context Protocol) enables AI agents to interact with external services securely. This kit provides:

- Pre-configured service connectors
- Setup scripts for quick deployment
- Secrets management structure

---

## Supported Services

| Service | File | Purpose |
|---------|------|---------|
| Cloudflare | `cloudflare.js` | CDN, DNS, Workers |
| Cloudinary | `cloudinary.js` | Image/video management |
| Figma | `figma.js` | Design file access |
| GitHub | `github.js` | Repository operations |
| Linear | `linear.js` | Issue tracking |
| MongoDB | `mongodb.js` | Database operations |
| Postman | `postman.js` | API testing |
| Sentry | `sentry.js` | Error monitoring |
| Supabase | `supabase.js` | Backend-as-a-Service |
| Vercel | `vercel.js` | Deployment platform |

---

## Setup

### Current Location

MCP Kit is now located at:
```
backend/src/integrations/mcp/
├── config/          # MCP configuration files
├── scripts/         # Setup and check scripts
├── secrets/         # Credentials (gitignored)
├── src/             # Service connectors
│   ├── services/    # Individual service modules
│   └── utils/       # Utility functions
└── README.md        # This file
```

### 1. Create secrets directory (if not exists)

```bash
chmod 700 backend/src/integrations/mcp/secrets
```

### 2. Configure MCP

Edit `config/mcp.json.example` and save as `.mcp.json` in project root:

```json
{
  "mcpServers": {
    "saas-gateway": {
      "command": "node",
      "args": ["/path/to/mcp-kit/mcp/services/dist/index.js"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}",
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 4. Set environment variables

Create `.env` with required tokens:

```bash
GITHUB_TOKEN=ghp_xxxxx
FIGMA_ACCESS_TOKEN=figd_xxxxx
CLOUDFLARE_API_TOKEN=xxxxx
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxxxx
```

### 5. Run setup script

```bash
cd mcp-kit/scripts/
./setup_mcp.sh
```

---

## File Structure

```
mcp/
├── README.md               # This file
├── README_MCP.md           # Detailed MCP documentation
├── config/
│   └── mcp.json.example    # Example configuration
├── services/
│   └── dist/               # Compiled service handlers
│       ├── index.js        # Main entry point
│       ├── services/       # Service modules
│       └── utils/          # Utilities (env, http, logger)
└── scripts/
    ├── setup_mcp.sh        # Initial setup
    ├── check_mcp.sh        # Health check
    └── link_mcp_config.sh  # Config linking
```

---

## Security Notes

- NEVER commit `.mcp.json` with real tokens
- Use `.env` files for secrets (add to `.gitignore`)
- Keep `secrets/` directory with restricted permissions
- Rotate tokens periodically

---

## Troubleshooting

### MCP not connecting

```bash
./scripts/check_mcp.sh
```

### Service errors

Check logs:
```bash
tail -f /tmp/mcp-saas-gateway.log
```

### Token issues

Verify environment:
```bash
echo $GITHUB_TOKEN | head -c 10
```

---

## Adding New Services

1. Create service file in `services/dist/services/`
2. Export handler functions
3. Register in `services/dist/index.js`
4. Add to MCP config

---

**Source:** uxcode-meet project
