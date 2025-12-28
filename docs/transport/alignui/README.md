# AlignUI Design System 2.0 - Transport Package

**Version:** 2.0
**Source:** AlignUI Figma Design System
**Pattern:** Radix UI Primitives + tailwind-variants (tv) + Polymorphic Components

---

## Overview

AlignUI is a comprehensive design system with 45+ React components built on:
- **Radix UI** - Accessible primitives
- **Tailwind CSS v4** - Utility-first styling with @theme tokens
- **tailwind-variants (tv)** - Type-safe variant management
- **Polymorphic components** - Flexible element rendering

---

## Package Contents

### /docs
Core documentation files:
- `ALIGNUI_COMPONENT_MAP.md` - Component API reference
- `AlignUI.json` - Machine-readable component registry
- `DESIGN_SYSTEM_MAP.md` - Full system overview (57 components)
- `V3-DESIGN_SYSTEM.md` - Design system v3 specification
- `UX_UI_SPEC.md` - Complete UX/UI specifications

### /tokens
Design token contracts:
- `TOKEN_CONTRACT.md` - Complete token reference
  - Primitive color palettes (10 colors × full scale)
  - Semantic tokens (bg-*, text-*, stroke-*)
  - Status tokens (error, success, warning, etc.)
  - Shadow tokens
  - Typography scale
  - Border radius

### /figma
Figma integration tools:
- `FIGMA_MCP_PLAYBOOK.md` - Operational contract for Figma-to-React
- `FIGMA_NODE_INDEX.json` - Node ID registry for all components

### /pdf
60 PDF files with visual component specifications from Figma.

### /components
MHTML web archives of component documentation.

### /components-reference
**45+ React component source files** ready to use:

| Component | File | Radix Primitive |
|-----------|------|-----------------|
| Alert | `alert.tsx` | - |
| Avatar | `avatar.tsx` | `@radix-ui/react-avatar` |
| Badge | `badge.tsx` | - |
| Button | `button.tsx` | `@radix-ui/react-slot` |
| Checkbox | `checkbox.tsx` | `@radix-ui/react-checkbox` |
| Divider | `divider.tsx` | - |
| Drawer | `drawer.tsx` | `@radix-ui/react-dialog` |
| Dropdown | `dropdown.tsx` | `@radix-ui/react-dropdown-menu` |
| Input | `input.tsx` | - |
| Label | `label.tsx` | `@radix-ui/react-label` |
| Modal | `modal.tsx` | `@radix-ui/react-dialog` |
| Pagination | `pagination.tsx` | - |
| Popover | `popover.tsx` | `@radix-ui/react-popover` |
| Progress | `progress-bar.tsx` | `@radix-ui/react-progress` |
| Radio | `radio.tsx` | `@radix-ui/react-radio-group` |
| Select | `select.tsx` | `@radix-ui/react-select` |
| Switch | `switch.tsx` | `@radix-ui/react-switch` |
| Table | `table.tsx` | - |
| Tabs | `tab-menu-horizontal.tsx` | `@radix-ui/react-tabs` |
| Textarea | `textarea.tsx` | - |
| Tooltip | `tooltip.tsx` | `@radix-ui/react-tooltip` |
| ...and 25+ more | | |

### /utils
Required utility functions:
- `cn.ts` - Class name merging (clsx + tailwind-merge)
- `tv.ts` - Tailwind variants wrapper
- `polymorphic.ts` - Polymorphic component types
- `recursive-clone-children.tsx` - React children utilities

### /templates
3 complete dashboard templates:
- `marketing-template-master/` - Marketing dashboards
- `template-finance-master/` - Finance/banking dashboards
- `template-hr-master/` - HR management dashboards

---

## Quick Integration

### 1. Install dependencies

```bash
npm install @radix-ui/react-avatar @radix-ui/react-checkbox \
  @radix-ui/react-dialog @radix-ui/react-dropdown-menu \
  @radix-ui/react-label @radix-ui/react-popover \
  @radix-ui/react-progress @radix-ui/react-radio-group \
  @radix-ui/react-scroll-area @radix-ui/react-select \
  @radix-ui/react-slider @radix-ui/react-slot \
  @radix-ui/react-switch @radix-ui/react-tabs \
  @radix-ui/react-toggle-group @radix-ui/react-tooltip \
  @remixicon/react clsx tailwind-merge tailwind-variants
```

### 2. Copy files

```bash
# Components
cp -r transport/alignui/components-reference/* \
  /path/to/project/frontend/src/components/alignui/

# Utils (required)
cp transport/alignui/utils/* \
  /path/to/project/frontend/src/utils/
```

### 3. Configure Tailwind

Add to `tailwind.config.ts`:
```typescript
export default {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      // See TOKEN_CONTRACT.md for full token list
    }
  }
}
```

### 4. Add CSS tokens

Copy @theme tokens to your `index.css`:
```css
@import "tailwindcss";

@theme {
  /* See TOKEN_CONTRACT.md for complete token definitions */
  --color-primary-base: hsl(217 91% 60%);
  --color-bg-white-0: hsl(0 0% 100%);
  --color-text-strong-950: hsl(221.54 31.71% 8.04%);
  /* ... */
}
```

---

## Component Usage Pattern

All components follow the compound component pattern:

```tsx
import * as ComponentName from '@/components/alignui/component-name';

<ComponentName.Root variant="..." size="...">
  <ComponentName.SubPart />
</ComponentName.Root>
```

### Example: Button

```tsx
import * as Button from '@/components/alignui/button';
import { RiAddLine } from '@remixicon/react';

<Button.Root variant="primary" mode="filled" size="medium">
  <Button.Icon as={RiAddLine} />
  <span>Create</span>
</Button.Root>
```

### Example: Select

```tsx
import * as Select from '@/components/alignui/select';

<Select.Root value={value} onValueChange={setValue}>
  <Select.Trigger>
    <Select.Value placeholder="Select..." />
  </Select.Trigger>
  <Select.Content>
    <Select.Item value="a">Option A</Select.Item>
    <Select.Item value="b">Option B</Select.Item>
  </Select.Content>
</Select.Root>
```

---

## Token Quick Reference

### Colors
- **Primary:** `bg-primary-base`, `text-primary-base`
- **Background:** `bg-bg-white-0`, `bg-bg-weak-50`, `bg-bg-strong-950`
- **Text:** `text-text-strong-950`, `text-text-sub-600`, `text-text-soft-400`
- **Stroke:** `ring-stroke-soft-200`, `ring-stroke-strong-950`
- **Status:** `bg-error-base`, `bg-success-base`, `bg-warning-base`

### Typography
- **Headings:** `text-title-h1` through `text-title-h6`
- **Labels:** `text-label-xl` through `text-label-xs`
- **Paragraphs:** `text-paragraph-xl` through `text-paragraph-xs`

### Shadows
- **Regular:** `shadow-regular-xs`, `shadow-regular-sm`, `shadow-regular-md`
- **Focus:** `shadow-button-primary-focus`, `shadow-button-error-focus`

### Border Radius
- **Standard:** `rounded-10` (10px), `rounded-20` (20px)

---

## Documentation Files Index

| File | Purpose |
|------|---------|
| `ALIGNUI_COMPONENT_MAP.md` | Verified component API with variants |
| `AlignUI.json` | JSON registry for automation |
| `DESIGN_SYSTEM_MAP.md` | 57-component overview with gaps |
| `TOKEN_CONTRACT.md` | Complete token definitions |
| `FIGMA_MCP_PLAYBOOK.md` | 1:1 Figma-to-React workflow |
| `FIGMA_NODE_INDEX.json` | Figma node IDs for all components |

---

**Source:** uxcode-meet project
**Figma File:** pEe3Tz3bjuUAja59htoQBr
