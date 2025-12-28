# Transport Kit - Universal Design System & Tools

**Version:** 1.0.0
**Last Updated:** 2025-12-18
**Purpose:** Portable assets for cross-project reuse

---

## Overview

This folder contains universal assets that can be transported to any new project:

```
transport/
├── mcp/              # MCP (Model Context Protocol) configuration
├── alignui/          # AlignUI Design System 2.0
└── animation/        # Anime.js animation framework
```

---

## Quick Start

### 1. MCP Integration

Copy `mcp/` folder to your project root and configure:

```bash
# Copy MCP kit
cp -r transport/mcp/ /path/to/new-project/mcp-kit/

# Setup (edit scripts as needed)
cd /path/to/new-project/mcp-kit/scripts/
./setup_mcp.sh
```

### 2. AlignUI Design System

Copy `alignui/` to your project's docs or integrate components:

```bash
# Copy documentation
cp -r transport/alignui/docs/ /path/to/new-project/docs/design-system/

# Copy component reference
cp -r transport/alignui/components-reference/ /path/to/new-project/frontend/src/components/alignui/

# Copy utilities (required for components)
cp transport/alignui/utils/*.ts /path/to/new-project/frontend/src/utils/
```

### 3. Animation Framework

Copy `animation/` and integrate with your frontend:

```bash
# Copy documentation
cp -r transport/animation/docs/ /path/to/new-project/.animation/

# Copy hooks and utils
cp transport/animation/hooks/* /path/to/new-project/frontend/src/hooks/
cp transport/animation/utils/* /path/to/new-project/frontend/src/utils/
```

---

## Folder Structure

### mcp/
```
mcp/
├── README_MCP.md           # MCP setup documentation
├── config/
│   └── mcp.json.example    # Example MCP configuration
├── services/               # SaaS gateway services
│   └── dist/               # Compiled services
│       ├── index.js
│       └── services/       # Individual service modules
│           ├── cloudflare.js
│           ├── cloudinary.js
│           ├── figma.js
│           ├── github.js
│           ├── linear.js
│           ├── mongodb.js
│           ├── sentry.js
│           ├── supabase.js
│           └── vercel.js
└── scripts/                # Setup scripts
    ├── setup_mcp.sh
    ├── check_mcp.sh
    └── link_mcp_config.sh
```

### alignui/
```
alignui/
├── docs/                   # Design system documentation
│   ├── ALIGNUI_COMPONENT_MAP.md
│   ├── AlignUI.json
│   ├── DESIGN_SYSTEM_MAP.md
│   ├── V3-DESIGN_SYSTEM.md
│   └── UX_UI_SPEC.md
├── tokens/                 # Design tokens
│   └── TOKEN_CONTRACT.md
├── figma/                  # Figma integration
│   ├── FIGMA_MCP_PLAYBOOK.md
│   └── FIGMA_NODE_INDEX.json
├── pdf/                    # Component PDF documentation (60 files)
├── components/             # MHTML component references
├── components-reference/   # React component source files (45+ components)
├── utils/                  # Required utility functions
│   ├── cn.ts              # Class name utility
│   ├── tv.ts              # Tailwind variants
│   ├── polymorphic.ts     # Polymorphic component types
│   └── recursive-clone-children.tsx
└── templates/              # Sectoral dashboard templates
    ├── marketing-template-master/
    ├── template-finance-master/
    └── template-hr-master/
```

### animation/
```
animation/
├── docs/                   # Animation documentation
│   ├── README.md          # Animation overview
│   ├── 00-index.md        # Index
│   ├── 01-foundations.md  # Core concepts
│   ├── 02-animation-basics.md
│   ├── 03-css-transforms-properties.md
│   ├── 04-values-types.md
│   ├── 05-timing-easing.md
│   ├── 06-keyframes-stagger.md
│   ├── 07-timeline.md
│   ├── 08-advanced-features.md
│   ├── 09-svg-text.md
│   ├── 10-utilities-engine.md
│   ├── ANIMATION_INTEGRATION.md
│   ├── ANIMATION_PLAYBOOK_ANIMEJS.md
│   └── MOTION_ANIMEJS.md
├── hooks/                  # React animation hooks
│   ├── useAnimation.ts
│   └── useAnimeMotion.ts
└── utils/                  # Animation utilities
    └── animations.ts
```

---

## Dependencies

### For AlignUI Components
```json
{
  "dependencies": {
    "@radix-ui/react-avatar": "^1.x",
    "@radix-ui/react-checkbox": "^1.x",
    "@radix-ui/react-dialog": "^1.x",
    "@radix-ui/react-dropdown-menu": "^1.x",
    "@radix-ui/react-label": "^1.x",
    "@radix-ui/react-popover": "^1.x",
    "@radix-ui/react-progress": "^1.x",
    "@radix-ui/react-radio-group": "^1.x",
    "@radix-ui/react-scroll-area": "^1.x",
    "@radix-ui/react-select": "^1.x",
    "@radix-ui/react-slider": "^1.x",
    "@radix-ui/react-slot": "^1.x",
    "@radix-ui/react-switch": "^1.x",
    "@radix-ui/react-tabs": "^1.x",
    "@radix-ui/react-toggle-group": "^1.x",
    "@radix-ui/react-tooltip": "^1.x",
    "@remixicon/react": "^4.x",
    "clsx": "^2.x",
    "tailwind-merge": "^2.x",
    "tailwind-variants": "^0.2.x"
  }
}
```

### For Animation Framework
```json
{
  "dependencies": {
    "animejs": "^4.x"
  }
}
```

---

## Integration Checklist

- [ ] Copy required folders to new project
- [ ] Install npm dependencies (see above)
- [ ] Configure Tailwind CSS with design tokens
- [ ] Copy `index.css` with @theme tokens
- [ ] Update import paths as needed
- [ ] Test component rendering
- [ ] Verify MCP services connection

---

## Support Files

Key configuration files you may also need from the source project:

- `frontend/tailwind.config.ts` - Tailwind configuration
- `frontend/src/index.css` - CSS tokens and @theme definitions
- `.mcp.json` - MCP configuration (DO NOT COMMIT - contains secrets)
- `.env.example` - Environment variable template

---

**Maintained by:** Claude Opus 4.5
**Source Project:** uxcode-meet
