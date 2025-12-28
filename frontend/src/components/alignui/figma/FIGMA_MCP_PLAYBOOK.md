# Figma MCP Playbook — AlignUI Design System Integration

**Version:** 1.0
**Last Updated:** 2025-12-18
**Target Agent:** Claude Opus 4.5
**Purpose:** Operational contract for 1:1 Figma-to-React implementation

---

## 1. Figma File Structure & Navigation

### 1.1 Master Design System File
```
File: Align-UI Design System 2.0
URL: https://www.figma.com/design/pEe3Tz3bjuUAja59htoQBr/
```

### 1.2 Key Sections & Node IDs

| Section | Node ID | Purpose |
|---------|---------|---------|
| Typography | `2697-307` | Font scales, text styles |
| Color Palette | `2623-2287` | All color tokens |
| Token System | `2645-344` | Semantic token mappings |
| Icons | `2716-25504` | Icon library |
| Shadows | `2767-1801` | Shadow tokens |
| Corner Radius | `2839-908` | Border radius tokens |
| Buttons | `2955-34374` | Button component variants |
| Avatar | `2906-13402` | Avatar component variants |
| Badge | `2939-17953` | Badge component variants |
| Modal | `3319-16461` | Modal component |
| Select | `3211-6627` | Select component |
| Switch | `3677-7838` | Switch component |

### 1.3 Search Strategies

#### By Component Name
```
1. Open Figma file in Dev Mode (keyboard: Shift+D)
2. Use Cmd/Ctrl+F to search
3. Search patterns:
   - "Button/Primary" → finds Button component sets
   - ".Component Name" → finds component definitions
   - "#variant-name" → finds specific variants
```

#### By Layer Name Heuristics
```
AlignUI naming convention:
- Component roots: "Component Name" (e.g., "Button", "Badge")
- Variants: "variant=value" (e.g., "variant=filled, size=medium")
- States: "state=hover", "state=focus", "state=disabled"
- Slots: "Icon", "Label", "Content"
```

---

## 2. Node Registry Protocol

### 2.1 Node ID Extraction

```
URL Pattern:
https://www.figma.com/design/{FILE_KEY}/{FILE_NAME}?node-id={NODE_ID}&m=dev

Example:
https://www.figma.com/design/pEe3Tz3bjuUAja59htoQBr/Align-UI?node-id=2955-34374&m=dev
                                                            └────────────┘
                                                               NODE_ID
```

### 2.2 Registry Format

```json
{
  "componentName": "Button",
  "figmaUrl": "https://www.figma.com/design/...",
  "nodeId": "2955-34374",
  "localFile": "frontend/src/components/alignui/button.tsx",
  "variants": {
    "variant": ["primary", "neutral", "error"],
    "mode": ["filled", "stroke", "lighter", "ghost"],
    "size": ["medium", "small", "xsmall", "xxsmall"]
  },
  "verified": true
}
```

### 2.3 When Node ID is Unknown

```markdown
STATUS: UNKNOWN
INSTRUCTION:
1. Open Figma Dev Mode on design system file
2. Navigate to Components panel (left sidebar)
3. Search: "{ComponentName}"
4. Right-click → Copy link
5. Extract node-id from URL
```

---

## 3. Token Extraction Pipeline

### 3.1 Figma Variables → CSS Variables

```
STEP 1: Extract from Figma Variables panel
  └── Collection: "Color" / "Typography" / "Spacing"
      └── Mode: "Light" / "Dark"
          └── Variable: name → value

STEP 2: Map to CSS Variables (index.css @theme block)
  --color-{category}-{shade}: hsl(H S% L%);

STEP 3: Reference in Tailwind config
  colors: {
    category: {
      'shade': 'hsl(var(--category-shade))'
    }
  }
```

### 3.2 Token Categories

| Figma Category | CSS Pattern | Tailwind Utility |
|----------------|-------------|------------------|
| Background | `--color-bg-{name}` | `bg-bg-{name}` |
| Text | `--color-text-{name}` | `text-text-{name}` |
| Stroke | `--color-stroke-{name}` | `border-stroke-{name}` |
| Primary | `--color-primary-{name}` | `bg-primary-{name}` |
| Semantic | `--color-{status}-{level}` | `bg-{status}-{level}` |

### 3.3 Alpha Token Handling

```css
/* Alpha tokens for transparency (critical for dark mode) */
--color-{palette}-alpha-24: hsl(H S% L% / 24%);
--color-{palette}-alpha-16: hsl(H S% L% / 16%);
--color-{palette}-alpha-10: hsl(H S% L% / 10%);
```

**Usage:** Hover states, focus rings, overlays

---

## 4. Component Variant Mapping

### 4.1 Figma Variant → React Props

```typescript
// Figma component set structure:
// Button / variant=primary, mode=filled, size=medium

// Maps to React component:
<Button.Root variant="primary" mode="filled" size="medium">
  <Button.Icon as={RiIconName} />
  <span>Label</span>
</Button.Root>
```

### 4.2 tv() Variant Detection

```bash
# Search for variants in component file:
grep -n "variants:" frontend/src/components/alignui/{component}.tsx

# Search for compound variants:
grep -n "compoundVariants" frontend/src/components/alignui/{component}.tsx

# List all exported parts:
grep -n "export {" frontend/src/components/alignui/{component}.tsx
```

### 4.3 Standard Variant Patterns

| Component | variant | mode | size | color |
|-----------|---------|------|------|-------|
| Button | primary, neutral, error | filled, stroke, lighter, ghost | medium, small, xsmall, xxsmall | - |
| Badge | filled, light, lighter, stroke | - | small, medium | gray, blue, orange, red, green, yellow, purple, sky, pink, teal |
| Avatar | - | - | 80, 72, 64, 56, 48, 40, 32, 24, 20 | gray, yellow, blue, sky, purple, red |
| Alert | filled, light, lighter, stroke | - | - | gray, blue, orange, red, green |

---

## 5. 1:1 Implementation Checklist (DoD)

### 5.1 Layout & Spacing

- [ ] Container max-width matches Figma frame
- [ ] Padding values exact (check Tailwind spacing scale)
- [ ] Gap between elements matches
- [ ] Margin/spacing tokens used (not arbitrary values)
- [ ] Responsive breakpoints defined

### 5.2 Typography

- [ ] Font family: Inter (via `font-sans`)
- [ ] Text size: `text-{scale}` matches Figma text style
- [ ] Line height: included in text scale token
- [ ] Letter spacing: included in text scale token
- [ ] Font weight: `font-{weight}` matches

### 5.3 Colors

- [ ] Background: semantic `bg-bg-{name}` tokens
- [ ] Text: semantic `text-text-{name}` tokens
- [ ] Borders: semantic `stroke-{name}` tokens
- [ ] No hardcoded hex values (use tokens)

### 5.4 States

- [ ] Default state matches Figma "Default"
- [ ] Hover state: `:hover` classes match Figma "Hover"
- [ ] Focus state: `focus-visible:` matches Figma "Focus"
- [ ] Disabled state: `disabled:` matches Figma "Disabled"
- [ ] Active/Pressed state if applicable

### 5.5 Dark Mode

- [ ] `dark:` variants added where needed
- [ ] Alpha tokens used for transparency
- [ ] Contrast ratios maintained (WCAG AA)

### 5.6 Responsive

- [ ] Mobile-first base styles
- [ ] `md:` breakpoint adjustments
- [ ] `lg:` breakpoint for desktop
- [ ] Touch targets minimum 44x44px on mobile

### 5.7 Accessibility

- [ ] Semantic HTML elements
- [ ] ARIA labels where needed
- [ ] Focus ring visible
- [ ] Color contrast sufficient
- [ ] Screen reader text for icons

---

## 6. "No Guessing" Protocol

### 6.1 Data Gaps Handling

```markdown
IF: Missing data (node-id, variant name, token value)
THEN:
  1. Mark as UNKNOWN in output
  2. Provide exact search command or Figma navigation path
  3. Do NOT invent values
  4. Continue with available data

EXAMPLE:
---
Component: DatePicker
Node ID: UNKNOWN
Instruction: Search "Date Picker" in Figma Dev Mode → Components panel
Variants: VERIFY IN CODE
  Command: grep -n "variants:" frontend/src/components/alignui/date-picker*.tsx
---
```

### 6.2 Verification Commands

```bash
# Check if component exists locally:
ls frontend/src/components/alignui/ | grep -i "{component}"

# Get component exports:
grep "export" frontend/src/components/alignui/{component}.tsx | head -20

# Get variant types:
grep -A 20 "variants:" frontend/src/components/alignui/{component}.tsx

# Verify token exists in CSS:
grep "{token-name}" frontend/src/index.css
```

### 6.3 Clarification Questions (Max 3)

When blocked, ask maximum 3 questions:

1. **Node ID Question:** "What is the Figma node-id for {Screen/Component}?"
2. **Variant Question:** "Which variant/mode should be used: A, B, or C?"
3. **Behavior Question:** "What should happen on {interaction}?"

---

## 7. Workflow Execution Order

```
┌─────────────────────────────────────────────────────────┐
│ 1. IDENTIFY                                             │
│    - Screen/component from Figma                        │
│    - Get node-id from URL                               │
│    - Document in FIGMA_NODE_INDEX.json                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. ANALYZE                                              │
│    - Extract layout structure (frames, groups)          │
│    - Identify AlignUI components used                   │
│    - Note custom elements needing composition           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. MAP TOKENS                                           │
│    - Colors → bg-*/text-*/stroke-*                      │
│    - Typography → text-{scale}                          │
│    - Spacing → p-*/m-*/gap-*                            │
│    - Shadows → shadow-{name}                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. IMPLEMENT                                            │
│    - Use existing AlignUI components (no rewrites)      │
│    - Compose with layout containers                     │
│    - Add state handling (hover/focus/disabled)          │
│    - Add responsive breakpoints                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. VERIFY                                               │
│    - npm run build (no errors)                          │
│    - Visual comparison to Figma                         │
│    - Test all states                                    │
│    - Test dark mode                                     │
│    - Test responsive                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 8. MCP Figma Integration Commands

### 8.1 Reading Node from Figma via MCP

```bash
# Get node content (requires figma-mcp configured)
figma-mcp fetch-node --file-id pEe3Tz3bjuUAja59htoQBr --node-id 2955-34374

# Export variables from Figma
figma-mcp export-variables --file-id pEe3Tz3bjuUAja59htoQBr --output tokens.json

# Get component properties
figma-mcp get-component --file-id pEe3Tz3bjuUAja59htoQBr --node-id 2955-34374
```

### 8.2 Quick Figma URL Generation

```javascript
// Generate Figma Dev Mode URL for any node-id
const nodeId = "2955-34374";
const url = `https://www.figma.com/design/pEe3Tz3bjuUAja59htoQBr/Align-UI?node-id=${nodeId}&m=dev`;
```

### 8.3 Batch Node Extraction

```bash
# Read from FIGMA_NODE_INDEX.json and verify all nodes
cat docs/FIGMA_NODE_INDEX.json | jq '.components[] | select(.localFile != null) | .nodeId'

# Find nodes missing local files
cat docs/FIGMA_NODE_INDEX.json | jq '.components[] | select(.localFile == null) | .name'
```

### 8.4 MCP Integration Pattern

```typescript
// Example: Using MCP in agent workflow
async function fetchFigmaNode(nodeId: string) {
  // 1. Fetch node via MCP
  const node = await figmaMcp.fetchNode({
    fileId: 'pEe3Tz3bjuUAja59htoQBr',
    nodeId: nodeId
  });

  // 2. Extract styles
  const styles = node.absoluteBoundingBox;
  const fills = node.fills;

  // 3. Map to tokens
  return mapToTokens(styles, fills);
}
```

---

## 9. Quick Reference

### Token Prefixes
```
bg-bg-       → Background colors
text-text-   → Text colors
stroke-      → Border colors
shadow-      → Box shadows
rounded-     → Border radius
```

### Typography Scale
```
text-title-h1..h6     → Headings
text-label-xl..xs     → Labels (medium weight)
text-paragraph-xl..xs → Body text (regular weight)
text-subheading-*     → Subheadings (uppercase tracking)
```

### Component Import Pattern
```typescript
import * as ComponentName from '@/components/alignui/component-name';

// Usage:
<ComponentName.Root {...props}>
  <ComponentName.SubPart />
</ComponentName.Root>
```

---

**Document Status:** Ready for agent consumption
**Next Steps:** See FIGMA_NODE_INDEX.json for specific screen mappings
