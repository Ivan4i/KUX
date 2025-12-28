# Transport Index - Quick Navigation

## MCP Kit
- [README](mcp/README.md)
- [Setup Guide](mcp/README_MCP.md)
- [Config Example](mcp/config/mcp.json.example)
- Scripts: `setup_mcp.sh`, `check_mcp.sh`

## AlignUI Design System
- [README](alignui/README.md)
- [Component Map](alignui/docs/ALIGNUI_COMPONENT_MAP.md)
- [Component JSON](alignui/docs/AlignUI.json)
- [Design System Map](alignui/docs/DESIGN_SYSTEM_MAP.md)
- [Token Contract](alignui/tokens/TOKEN_CONTRACT.md)
- [Figma Playbook](alignui/figma/FIGMA_MCP_PLAYBOOK.md)
- [Figma Node Index](alignui/figma/FIGMA_NODE_INDEX.json)
- PDF docs: `alignui/pdf/` (60 files)
- Components: `alignui/components-reference/` (45+ files)
- Utils: `alignui/utils/` (cn, tv, polymorphic)
- Templates: `alignui/templates/` (3 dashboards)

## Animation
- [README](animation/README.md)
- [Index](animation/docs/00-index.md)
- [Foundations](animation/docs/01-foundations.md)
- [Basics](animation/docs/02-animation-basics.md)
- [AlignUI Integration](animation/docs/ANIMATION_INTEGRATION.md)
- [Playbook](animation/docs/ANIMATION_PLAYBOOK_ANIMEJS.md)
- Hooks: `useAnimation.ts`, `useAnimeMotion.ts`
- Utils: `animations.ts`

---

## Copy Commands

```bash
# Full transport
cp -r transport/ /new-project/

# MCP only
cp -r transport/mcp/ /new-project/mcp-kit/

# AlignUI only
cp -r transport/alignui/ /new-project/docs/design-system/

# Animation only
cp -r transport/animation/ /new-project/.animation/
```
