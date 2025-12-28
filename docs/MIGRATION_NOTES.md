# Migration Notes - Documentation & Transport Restructure

**Date:** 2024-12-28
**Branch:** feature/docs-restructure

## Summary

This migration restructured the documentation and relocated transport assets (AlignUI, MCP Kit, animations) from the old `docs/transport/` location to their proper architectural homes.

---

## What Moved

### 1. Documentation (45 files)

| From | To |
|------|-----|
| `new docs/*.md` | `docs/*.md` |
| `new docs/*.json` | `docs/*.json` |

The 45 numbered documentation files (00-91 series) are now the single source of truth in `docs/`.

### 2. AlignUI Design System (~2000 files)

| From | To |
|------|-----|
| `docs/transport/alignui/` | `frontend/src/components/alignui/` |

**Status:** Parked (excluded from TypeScript compilation)

AlignUI components are present but excluded from build via `tsconfig.json` exclude rules. This prevents build failures from missing dependencies while keeping assets available for future integration.

**To integrate AlignUI:**
1. Install dependencies (see `frontend/src/components/alignui/README.md`)
2. Add path aliases to `tsconfig.json`
3. Remove exclusions from `tsconfig.json`

### 3. MCP Kit (Node.js service)

| From | To |
|------|-----|
| `docs/transport/mcp/` | `tools/mcp/` |
| (incorrectly placed in `backend/src/integrations/mcp/`) | `tools/mcp/` |

**Reason for relocation:** MCP Kit is a Node.js/TypeScript service, not a Python module. Placing it in the Python backend's `src/` directory was architecturally incorrect. Now located at project root level in `tools/`.

### 4. Animation Library

| From | To |
|------|-----|
| `docs/transport/animation/` | `frontend/src/lib/animations/` |

**Status:** Parked (excluded from TypeScript compilation)

Animation hooks and utilities are present but excluded from build. Integrate when ready by removing exclusions.

---

## Deleted Folders

- `docs/architecture/` (old, outdated)
- `docs/planning/` (old, outdated)
- `docs/progress/` (old, outdated)
- `docs/setup/` (old, outdated)
- `docs/transport/` (assets relocated)
- `new docs/` (content migrated to `docs/`)

---

## Configuration Changes

### frontend/tsconfig.json

Added exclude rules to prevent AlignUI/animations from breaking builds:

```json
"exclude": [
  "src/components/alignui/**/*",
  "src/lib/animations/**/*"
]
```

### .gitignore

Updated path for large AlignUI PDF files:

```
frontend/src/components/alignui/pdf/Icons*.pdf
```

---

## Verification Commands

```bash
# Check for stale references
grep -r "docs/transport" . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=venv
grep -r "new docs" . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=venv

# Verify TypeScript compiles (AlignUI excluded)
cd frontend && npx tsc --noEmit

# Verify docs structure
ls docs/ | wc -l  # Should be 46 (45 files + MIGRATION_NOTES.md)
```

---

## Entry Points

- **Documentation:** `docs/README_START_HERE.md`
- **Quick Links:** `docs/QUICK_LINKS.md`
- **Project Index:** `docs/00_PROJECT_INDEX.json`
- **AlignUI:** `frontend/src/components/alignui/README.md`
- **MCP Kit:** `tools/mcp/README.md`
- **Animations:** `frontend/src/lib/animations/README.md`
