# Changelog

All notable changes to the Transport Kit.

## [1.0.0] - 2025-12-18

### Added

**MCP Kit** (29 source files + configs + secrets)
- SaaS Gateway with 13 service connectors:
  - cloudflare, cloudinary, figma, github, linear
  - mongodb, monitoring, notion, postman, sentry
  - stubs, supabase, vercel
- TypeScript source files (src/)
- Setup and check scripts
- **Full secrets bundle:**
  - `.env.local` with all tokens
  - `.env.root` (project root env)
  - `mcp.json` (full MCP config)
  - `box_private_key.pem`
  - `.credentials`

**AlignUI Design System** (~200 files)
- 45+ React components (Radix UI + tailwind-variants)
- 59 PDF component specifications
- Design tokens (TOKEN_CONTRACT.md)
- Figma integration (FIGMA_MCP_PLAYBOOK.md, NODE_INDEX.json)
- 3 sectoral dashboard templates (Marketing, Finance, HR)
- MHTML component references
- Utility functions (cn, tv, polymorphic)

**Animation Framework** (~20 files)
- 14 anime.js documentation guides
- React hooks (useAnimation, useAnimeMotion)
- Animation utilities
- AlignUI integration patterns

### Package Structure
```
transport/
├── README.md
├── TRANSPORT_INDEX.md
├── CHANGELOG.md
├── .gitignore
│
├── mcp/
│   ├── config/
│   │   ├── .env.local          # REAL TOKENS
│   │   ├── .env.root           # Project root env
│   │   ├── .env.example        # Template
│   │   └── mcp.json            # Full MCP config
│   ├── secrets/
│   │   ├── .credentials
│   │   └── box_private_key.pem
│   ├── src/                    # TypeScript sources
│   └── scripts/                # Setup scripts
│
├── alignui/
│   ├── docs/
│   ├── tokens/
│   ├── figma/
│   ├── pdf/
│   ├── components-reference/
│   ├── utils/
│   └── templates/
│
└── animation/
    ├── docs/
    ├── hooks/
    └── utils/
```

### Usage

```bash
# Copy entire transport kit
cp -r transport/ /path/to/new-project/

# Setup MCP in new project
cd /path/to/new-project/transport/mcp
npm install
npm run build
cp config/.env.local ../../.env.local
cp config/mcp.json ../../.mcp.json
```

### Security Warning

This transport kit contains REAL API TOKENS AND SECRETS.
- Only copy to your own machines/repos
- Never commit to public repositories
- See `.gitignore` for what to exclude if going public

---

## Dependencies Required

```json
{
  "mcp": {
    "@modelcontextprotocol/sdk": "^1.x",
    "zod": "^3.x",
    "typescript": "^5.x"
  },
  "alignui": {
    "@radix-ui/react-*": "^1.x",
    "@remixicon/react": "^4.x",
    "tailwind-variants": "^0.2.x",
    "clsx": "^2.x",
    "tailwind-merge": "^2.x"
  },
  "animation": {
    "animejs": "^4.x"
  }
}
```
