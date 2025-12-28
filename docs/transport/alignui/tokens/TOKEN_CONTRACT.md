# AlignUI Token Contract — Design System Token Reference

**Version:** 1.0
**Last Updated:** 2025-12-18
**Source of Truth:** `frontend/src/index.css` (Tailwind v4 @theme directive)
**Pattern:** CSS Custom Properties → Tailwind @theme → Utility Classes

---

## Architecture Overview

### Token Pipeline
```
Figma Variables → CSS Custom Properties → Tailwind @theme → Utility Classes
       ↓                    ↓                    ↓                ↓
   Color Palette      --color-*           @theme block        bg-*, text-*
   Token System       --shadow-*          CSS Variables       shadow-*
   Typography         --font-*            Auto-generated      text-title-h5
```

### Tailwind v4 Integration
```css
@import "tailwindcss";
@config "../tailwind.config.ts";

@theme {
  --color-primary-base: var(--color-blue-500);
  /* CSS variable becomes utility: bg-primary-base */
}
```

---

## Token Groups

### 1. Primitive Color Palettes

Each color has full scale (50-950) plus alpha variants:

| Palette | Scale | Alpha Variants | Example |
|---------|-------|----------------|---------|
| neutral | 0, 50-950 | alpha-24, alpha-16, alpha-10 | `--color-neutral-500` |
| blue | 50-950 | alpha-24, alpha-16, alpha-10 | `--color-blue-500` |
| orange | 50-950 | alpha-24, alpha-16, alpha-10 | `--color-orange-500` |
| red | 50-950 | alpha-24, alpha-16, alpha-10 | `--color-red-500` |
| green | 50-950 | alpha-24, alpha-16, alpha-10 | `--color-green-500` |
| yellow | 50-950 | alpha-24, alpha-16, alpha-10 | `--color-yellow-500` |
| purple | 50-950 | alpha-24, alpha-16, alpha-10 | `--color-purple-500` |
| teal | 50-950 | alpha-24, alpha-16, alpha-10 | `--color-teal-500` |
| sky | 50-950 | alpha-24, alpha-16, alpha-10 | `--color-sky-500` |
| pink | 50-950 | alpha-24, alpha-16, alpha-10 | `--color-pink-500` |

#### Primitive Token Example
```css
@theme {
  /* Neutral scale */
  --color-neutral-0: hsl(0 0% 100%);
  --color-neutral-50: hsl(216 33.33% 97.06%);
  --color-neutral-100: hsl(210 30% 96.08%);
  --color-neutral-200: hsl(220 17.65% 90%);
  --color-neutral-300: hsl(218.57 15.22% 81.96%);
  --color-neutral-400: hsl(220 11.48% 64.12%);
  --color-neutral-500: hsl(221.05 7.76% 48.04%);
  --color-neutral-600: hsl(222 10.87% 36.08%);
  --color-neutral-700: hsl(221.25 15.69% 20%);
  --color-neutral-800: hsl(227.14 17.07% 16.08%);
  --color-neutral-900: hsl(226.15 21.31% 11.96%);
  --color-neutral-950: hsl(221.54 31.71% 8.04%);

  /* Alpha variants for transparency effects */
  --color-neutral-alpha-24: hsl(220 11.48% 64.12% / 24%);
  --color-neutral-alpha-16: hsl(220 11.48% 64.12% / 16%);
  --color-neutral-alpha-10: hsl(220 11.48% 64.12% / 10%);
}
```

---

### 2. Primary Brand Tokens

| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-primary-dark` | `blue-800` | `text-primary-dark`, `bg-primary-dark` |
| `--color-primary-darker` | `blue-700` | `text-primary-darker`, `bg-primary-darker` |
| `--color-primary-base` | `blue-500` | `text-primary-base`, `bg-primary-base` |
| `--color-primary-alpha-24` | `blue-alpha-24` | `bg-primary-alpha-24` |
| `--color-primary-alpha-16` | `blue-alpha-16` | `bg-primary-alpha-16` |
| `--color-primary-alpha-10` | `blue-alpha-10` | `bg-primary-alpha-10` |

#### Usage Example
```tsx
// Primary button
<button className="bg-primary-base hover:bg-primary-darker text-static-white">
  Click me
</button>

// Primary with alpha background
<div className="bg-primary-alpha-10 p-4">
  <Icon className="text-primary-base" />
</div>
```

---

### 3. Static Tokens

Fixed colors that don't change between light/dark modes:

| Token | Value | Utility Class |
|-------|-------|---------------|
| `--color-static-black` | `neutral-950` | `text-static-black`, `bg-static-black` |
| `--color-static-white` | `neutral-0` | `text-static-white`, `bg-static-white` |

---

### 4. Semantic Background (bg-*) Tokens

| Token | Source | Utility Class | Use Case |
|-------|--------|---------------|----------|
| `--color-bg-strong-950` | `neutral-950` | `bg-bg-strong-950` | Dark backgrounds, tooltips |
| `--color-bg-surface-800` | `neutral-800` | `bg-bg-surface-800` | Dark surface panels |
| `--color-bg-sub-300` | `neutral-300` | `bg-bg-sub-300` | Switch thumb background |
| `--color-bg-soft-200` | `neutral-200` | `bg-bg-soft-200` | Unchecked switches, dividers |
| `--color-bg-weak-50` | `neutral-50` | `bg-bg-weak-50` | Page background, disabled states |
| `--color-bg-white-0` | `neutral-0` | `bg-bg-white-0` | Cards, content areas |

#### Background Token Hierarchy (light to dark)
```
white-0 → weak-50 → soft-200 → sub-300 → surface-800 → strong-950
  ↓         ↓          ↓          ↓           ↓            ↓
 Cards   Page BG    Dividers   Toggles    Dark UI     Tooltips
```

---

### 5. Semantic Text (text-*) Tokens

| Token | Source | Utility Class | Use Case |
|-------|--------|---------------|----------|
| `--color-text-strong-950` | `neutral-950` | `text-text-strong-950` | Primary text, headings |
| `--color-text-sub-600` | `neutral-600` | `text-text-sub-600` | Secondary text, descriptions |
| `--color-text-soft-400` | `neutral-400` | `text-text-soft-400` | Placeholder text, hints |
| `--color-text-disabled-300` | `neutral-300` | `text-text-disabled-300` | Disabled state text |
| `--color-text-white-0` | `neutral-0` | `text-text-white-0` | Text on dark backgrounds |

#### Text Token Hierarchy (high to low contrast)
```
strong-950 → sub-600 → soft-400 → disabled-300 → white-0
    ↓           ↓          ↓            ↓            ↓
 Headings    Body text  Placeholders  Disabled   On dark BG
```

---

### 6. Semantic Stroke (stroke-*) Tokens

| Token | Source | Utility Class | Use Case |
|-------|--------|---------------|----------|
| `--color-stroke-strong-950` | `neutral-950` | `ring-stroke-strong-950` | Focus rings, emphasis |
| `--color-stroke-sub-300` | `neutral-300` | `ring-stroke-sub-300` | Secondary borders |
| `--color-stroke-soft-200` | `neutral-200` | `ring-stroke-soft-200` | Default borders, dividers |
| `--color-stroke-white-0` | `neutral-0` | `ring-stroke-white-0` | Light borders on dark |

#### Usage Example
```tsx
// Default input border
<input className="ring-1 ring-stroke-soft-200 focus:ring-stroke-strong-950" />

// Card with soft border
<div className="rounded-20 border border-stroke-soft-200 bg-bg-white-0" />
```

---

### 7. Semantic Status Tokens

Each status has 4 levels: `dark`, `base`, `light`, `lighter`

#### Faded (gray/neutral states)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-faded-dark` | `neutral-800` | `text-faded-dark`, `bg-faded-dark` |
| `--color-faded-base` | `neutral-500` | `text-faded-base`, `bg-faded-base` |
| `--color-faded-light` | `neutral-200` | `bg-faded-light` |
| `--color-faded-lighter` | `neutral-100` | `bg-faded-lighter` |

#### Information (blue)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-information-dark` | `blue-950` | `text-information-dark` |
| `--color-information-base` | `blue-500` | `text-information-base`, `bg-information-base` |
| `--color-information-light` | `blue-200` | `bg-information-light` |
| `--color-information-lighter` | `blue-50` | `bg-information-lighter` |

#### Warning (orange)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-warning-dark` | `orange-950` | `text-warning-dark` |
| `--color-warning-base` | `orange-500` | `text-warning-base`, `bg-warning-base` |
| `--color-warning-light` | `orange-200` | `bg-warning-light` |
| `--color-warning-lighter` | `orange-50` | `bg-warning-lighter` |

#### Error (red)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-error-dark` | `red-950` | `text-error-dark` |
| `--color-error-base` | `red-500` | `text-error-base`, `bg-error-base` |
| `--color-error-light` | `red-200` | `bg-error-light` |
| `--color-error-lighter` | `red-50` | `bg-error-lighter` |

#### Success (green)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-success-dark` | `green-950` | `text-success-dark` |
| `--color-success-base` | `green-500` | `text-success-base`, `bg-success-base` |
| `--color-success-light` | `green-200` | `bg-success-light` |
| `--color-success-lighter` | `green-50` | `bg-success-lighter` |

#### Away (yellow)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-away-dark` | `yellow-950` | `text-away-dark` |
| `--color-away-base` | `yellow-500` | `text-away-base`, `bg-away-base` |
| `--color-away-light` | `yellow-200` | `bg-away-light` |
| `--color-away-lighter` | `yellow-50` | `bg-away-lighter` |

#### Feature (purple)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-feature-dark` | `purple-950` | `text-feature-dark` |
| `--color-feature-base` | `purple-500` | `text-feature-base`, `bg-feature-base` |
| `--color-feature-light` | `purple-200` | `bg-feature-light` |
| `--color-feature-lighter` | `purple-50` | `bg-feature-lighter` |

#### Verified (sky)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-verified-dark` | `sky-950` | `text-verified-dark` |
| `--color-verified-base` | `sky-500` | `text-verified-base`, `bg-verified-base` |
| `--color-verified-light` | `sky-200` | `bg-verified-light` |
| `--color-verified-lighter` | `sky-50` | `bg-verified-lighter` |

#### Highlighted (pink)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-highlighted-dark` | `pink-950` | `text-highlighted-dark` |
| `--color-highlighted-base` | `pink-500` | `text-highlighted-base`, `bg-highlighted-base` |
| `--color-highlighted-light` | `pink-200` | `bg-highlighted-light` |
| `--color-highlighted-lighter` | `pink-50` | `bg-highlighted-lighter` |

#### Stable (teal)
| Token | Source | Utility Class |
|-------|--------|---------------|
| `--color-stable-dark` | `teal-950` | `text-stable-dark` |
| `--color-stable-base` | `teal-500` | `text-stable-base`, `bg-stable-base` |
| `--color-stable-light` | `teal-200` | `bg-stable-light` |
| `--color-stable-lighter` | `teal-50` | `bg-stable-lighter` |

---

### 8. Status Token Pattern

```
*-dark     → Text on light background badges
*-base     → Icon color, filled badge background, ring color
*-light    → "light" variant badge background
*-lighter  → "lighter" variant badge background
```

#### Badge Example
```tsx
// Filled badge (success)
<Badge.Root variant="filled" color="green">
  {/* bg-success-base text-static-white */}
</Badge.Root>

// Light badge (success)
<Badge.Root variant="light" color="green">
  {/* bg-success-light text-success-dark */}
</Badge.Root>

// Lighter badge (success)
<Badge.Root variant="lighter" color="green">
  {/* bg-success-lighter text-success-base */}
</Badge.Root>
```

---

## Alpha Tokens & Their Role

### Alpha Token Levels

| Level | Opacity | Use Case |
|-------|---------|----------|
| `alpha-24` | 24% | Hover states, selection backgrounds |
| `alpha-16` | 16% | Focus ring outer glow |
| `alpha-10` | 10% | Subtle backgrounds, disabled overlays |

### Alpha Token Applications

```css
/* Focus shadows using alpha tokens */
--shadow-button-primary-focus:
  0 0 0 2px var(--color-bg-white-0),      /* Inner ring - solid white */
  0 0 0 4px var(--color-primary-alpha-10); /* Outer glow - 10% primary */

--shadow-button-important-focus:
  0 0 0 2px var(--color-bg-white-0),
  0 0 0 4px var(--color-neutral-alpha-16); /* 16% neutral for neutral buttons */

--shadow-button-error-focus:
  0 0 0 2px var(--color-bg-white-0),
  0 0 0 4px var(--color-red-alpha-10);     /* 10% red for error states */
```

### Usage Example
```tsx
// Icon container with alpha background
<div className="flex size-10 items-center justify-center rounded-10 bg-primary-alpha-10">
  <RiVideoOnLine className="size-5 text-primary-base" />
</div>

// Selection state
<div className="bg-blue-alpha-24 rounded-lg p-2">
  Selected item
</div>
```

---

## Shadow Tokens

| Token | Value | Utility Class | Use Case |
|-------|-------|---------------|----------|
| `--shadow-regular-xs` | `0 1px 2px 0 #0a0d1408` | `shadow-regular-xs` | Buttons, inputs |
| `--shadow-regular-sm` | `0 2px 4px #1b1c1d0a` | `shadow-regular-sm` | Elevated cards |
| `--shadow-regular-md` | `0 16px 32px -12px #0e121b1a` | `shadow-regular-md` | Modals, dropdowns |
| `--shadow-button-primary-focus` | `0 0 0 2px... 4px...` | `shadow-button-primary-focus` | Primary button focus |
| `--shadow-button-important-focus` | `0 0 0 2px... 4px...` | `shadow-button-important-focus` | Neutral button focus |
| `--shadow-button-error-focus` | `0 0 0 2px... 4px...` | `shadow-button-error-focus` | Error button/input focus |
| `--shadow-toggle-switch` | `0 6px 10px...` | `shadow-toggle-switch` | Switch component |
| `--shadow-switch-thumb` | `0 4px 8px...` | `shadow-switch-thumb` | Switch thumb |
| `--shadow-tooltip` | `0 12px 24px...` | `shadow-tooltip` | Tooltips, popovers |

---

## Border Radius Tokens

| Token | Value | Utility Class |
|-------|-------|---------------|
| `--radius-10` | `0.625rem` (10px) | `rounded-10` |
| `--radius-20` | `1.25rem` (20px) | `rounded-20` |

Standard Tailwind radii also available: `rounded-lg` (8px), `rounded-xl` (12px), `rounded-2xl` (16px)

---

## Typography Tokens

### Font Family
```css
--font-family-sans: 'Inter', system-ui, -apple-system, sans-serif;
```

### Title Scale
| Token | Size | Utility Class |
|-------|------|---------------|
| `--font-size-title-h1` | 3.5rem (56px) | `text-title-h1` |
| `--font-size-title-h2` | 3rem (48px) | `text-title-h2` |
| `--font-size-title-h3` | 2.5rem (40px) | `text-title-h3` |
| `--font-size-title-h4` | 2rem (32px) | `text-title-h4` |
| `--font-size-title-h5` | 1.5rem (24px) | `text-title-h5` |
| `--font-size-title-h6` | 1.25rem (20px) | `text-title-h6` |

### Label Scale
| Token | Size | Utility Class |
|-------|------|---------------|
| `--font-size-label-xl` | 1.5rem (24px) | `text-label-xl` |
| `--font-size-label-lg` | 1.125rem (18px) | `text-label-lg` |
| `--font-size-label-md` | 1rem (16px) | `text-label-md` |
| `--font-size-label-sm` | 0.875rem (14px) | `text-label-sm` |
| `--font-size-label-xs` | 0.75rem (12px) | `text-label-xs` |

### Paragraph Scale
| Token | Size | Utility Class |
|-------|------|---------------|
| `--font-size-paragraph-xl` | 1.5rem (24px) | `text-paragraph-xl` |
| `--font-size-paragraph-lg` | 1.125rem (18px) | `text-paragraph-lg` |
| `--font-size-paragraph-md` | 1rem (16px) | `text-paragraph-md` |
| `--font-size-paragraph-sm` | 0.875rem (14px) | `text-paragraph-sm` |
| `--font-size-paragraph-xs` | 0.75rem (12px) | `text-paragraph-xs` |

### Subheading Scale
| Token | Size | Utility Class |
|-------|------|---------------|
| `--font-size-subheading-md` | 1rem (16px) | `text-subheading-md` |
| `--font-size-subheading-sm` | 0.875rem (14px) | `text-subheading-sm` |
| `--font-size-subheading-xs` | 0.75rem (12px) | `text-subheading-xs` |
| `--font-size-subheading-2xs` | 0.6875rem (11px) | `text-subheading-2xs` |

---

## Naming Convention Rules

### Pattern
```
--color-{category}-{variant}-{level}
```

### Categories
| Category | Examples |
|----------|----------|
| Primitive palettes | `neutral`, `blue`, `orange`, `red`, etc. |
| Primary brand | `primary` |
| Static | `static` |
| Semantic bg | `bg` |
| Semantic text | `text` |
| Semantic stroke | `stroke` |
| Semantic status | `faded`, `information`, `warning`, `error`, `success`, etc. |

### Levels
| Level Range | Meaning |
|-------------|---------|
| 0 | Pure white |
| 50-100 | Very light (background tints) |
| 200-300 | Light (borders, disabled) |
| 400-500 | Base (primary usage) |
| 600-700 | Medium (secondary text) |
| 800-950 | Dark (primary text, dark UI) |

### Examples
```css
/* Primitive */
--color-blue-500          /* Blue palette, base level */
--color-neutral-alpha-16  /* Neutral with 16% opacity */

/* Semantic background */
--color-bg-strong-950     /* Strong/dark background */
--color-bg-weak-50        /* Weak/light background */

/* Semantic text */
--color-text-strong-950   /* High contrast text */
--color-text-soft-400     /* Low contrast text */

/* Semantic status */
--color-error-base        /* Primary error color */
--color-error-lighter     /* Lightest error background */
```

---

## Light/Dark Mode Strategy

### Current Implementation: Light Mode Only

The current implementation uses semantic tokens mapped to light mode values. All tokens reference primitive values designed for light backgrounds.

### Dark Mode Preparation

When implementing dark mode, semantic tokens will be reassigned:

```css
/* Light mode (current) */
@theme {
  --color-bg-white-0: var(--color-neutral-0);      /* White background */
  --color-text-strong-950: var(--color-neutral-950); /* Dark text */
}

/* Dark mode (future) */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-white-0: var(--color-neutral-900);     /* Dark background */
    --color-text-strong-950: var(--color-neutral-50); /* Light text */
  }
}
```

### Dark Mode Alpha Tokens

Alpha tokens become critical for dark mode overlays:
- `alpha-24`: Selection states on dark backgrounds
- `alpha-16`: Focus glows on dark backgrounds
- `alpha-10`: Subtle overlays, glass effects

---

## Tailwind v4 Mapping

### @theme Directive

Tailwind v4 uses CSS-native `@theme` directive instead of JS config for colors:

```css
@theme {
  /* This creates: bg-primary-base, text-primary-base, border-primary-base */
  --color-primary-base: var(--color-blue-500);

  /* This creates: shadow-regular-xs */
  --shadow-regular-xs: 0 1px 2px 0 #0a0d1408;

  /* This creates: rounded-10 */
  --radius-10: 0.625rem;
}
```

### Token → Utility Mapping

| CSS Variable Pattern | Generated Utilities |
|---------------------|---------------------|
| `--color-*` | `bg-*`, `text-*`, `border-*`, `ring-*` |
| `--shadow-*` | `shadow-*` |
| `--radius-*` | `rounded-*` |
| `--font-size-*` | `text-*` |

### Usage in Components

```tsx
// All these utilities are auto-generated from @theme:
<div className={cn(
  // Background from --color-bg-white-0
  'bg-bg-white-0',
  // Border from --color-stroke-soft-200
  'ring-1 ring-stroke-soft-200',
  // Shadow from --shadow-regular-xs
  'shadow-regular-xs',
  // Radius from --radius-20
  'rounded-20',
  // Text from --color-text-strong-950
  'text-text-strong-950',
)}>
  Card content
</div>
```

---

## Verification Commands

```bash
# List all color tokens
grep "^  --color-" frontend/src/index.css

# List all shadow tokens
grep "^  --shadow-" frontend/src/index.css

# Find semantic token mappings
grep "var(--color-" frontend/src/index.css

# Find alpha token usage in components
grep "alpha-" frontend/src/components/alignui/*.tsx

# Verify token usage in a specific component
grep "bg-\|text-\|ring-" frontend/src/components/alignui/button.tsx
```

---

## Quick Reference Card

### Most Used Tokens

| Context | Token | Utility |
|---------|-------|---------|
| Page background | `bg-weak-50` | `bg-bg-weak-50` |
| Card background | `bg-white-0` | `bg-bg-white-0` |
| Primary text | `text-strong-950` | `text-text-strong-950` |
| Secondary text | `text-sub-600` | `text-text-sub-600` |
| Placeholder | `text-soft-400` | `text-text-soft-400` |
| Default border | `stroke-soft-200` | `ring-stroke-soft-200` |
| Focus border | `stroke-strong-950` | `ring-stroke-strong-950` |
| Primary action | `primary-base` | `bg-primary-base` |
| Primary hover | `primary-darker` | `hover:bg-primary-darker` |
| Error state | `error-base` | `ring-error-base` |
| Disabled | `text-disabled-300` | `text-text-disabled-300` |

---

**Document Status:** Ready for agent consumption
**Maintenance:** Update when tokens are added or dark mode is implemented
