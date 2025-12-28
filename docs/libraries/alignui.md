# AlignUI Design System

**Location:** `frontend/src/components/alignui/`
**Status:** Parked (excluded from TypeScript compilation until integration)

---

## Overview

AlignUI is a comprehensive design system with 45+ React components built on:
- Radix UI primitives
- Tailwind CSS v4
- tailwind-variants (tv)
- Polymorphic components

---

## Documentation Files

| File | Location |
|------|----------|
| README | `frontend/src/components/alignui/README.md` |
| Component Map | `frontend/src/components/alignui/docs/ALIGNUI_COMPONENT_MAP.md` |
| Design System Map | `frontend/src/components/alignui/docs/DESIGN_SYSTEM_MAP.md` |
| Token Contract | `frontend/src/components/alignui/tokens/TOKEN_CONTRACT.md` |
| Figma Playbook | `frontend/src/components/alignui/figma/FIGMA_MCP_PLAYBOOK.md` |
| Component JSON | `frontend/src/components/alignui/docs/AlignUI.json` |
| Figma Node Index | `frontend/src/components/alignui/figma/FIGMA_NODE_INDEX.json` |

---

## Directory Structure

```
frontend/src/components/alignui/
├── components-reference/    # 45+ React components
├── utils/                   # cn, tv, polymorphic utilities
├── tokens/                  # Design token contracts
├── config/                  # Tailwind/PostCSS configs
├── docs/                    # Component documentation
├── figma/                   # Figma integration
├── pdf/                     # 57 visual specifications
├── components/              # MHTML block references
└── templates/               # 3 dashboard templates
    ├── marketing-template-master/
    ├── template-finance-master/
    └── template-hr-master/
```

---

## Integration

To enable AlignUI in the build:

1. Install dependencies:
```bash
cd frontend
npm install @radix-ui/react-avatar @radix-ui/react-checkbox \
  @radix-ui/react-dialog @radix-ui/react-dropdown-menu \
  @radix-ui/react-slot @radix-ui/react-tooltip \
  @remixicon/react clsx tailwind-merge tailwind-variants
```

2. Add path aliases to `tsconfig.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/components/alignui/*": ["./src/components/alignui/components-reference/*"],
      "@/utils/*": ["./src/components/alignui/utils/*"]
    }
  }
}
```

3. Remove exclusions from `tsconfig.json`:
```json
// Remove this line:
"src/components/alignui/**/*"
```

---

## See Also

- Main integration guide: `docs/frontend/73_ALIGNUI_INTEGRATION.md`
- Design system reference: Token Contract, Component Map
