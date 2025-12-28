# AlignUI Component Map — React Implementation Reference

**Version:** 1.0
**Last Updated:** 2025-12-18
**Source of Truth:** `frontend/src/components/alignui/*.tsx`
**Pattern:** Radix UI Primitives + tailwind-variants (tv) + Polymorphic Components

---

## Architecture Overview

### Component Structure Pattern
```
frontend/src/components/alignui/
├── {component}.tsx         # Main component with tv() variants
├── index.ts                # Re-exports
└── {component}-*.tsx       # Subcomponents/variants
```

### Common Imports
```typescript
import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { tv, type VariantProps } from '@/utils/tv';
import { cnExt } from '@/utils/cn';
import type { PolymorphicComponentProps } from '@/utils/polymorphic';
import { recursiveCloneChildren } from '@/utils/recursive-clone-children';
```

### Component Usage Pattern
```typescript
import * as ComponentName from '@/components/alignui/component-name';

<ComponentName.Root variant="..." size="...">
  <ComponentName.SubPart />
</ComponentName.Root>
```

---

## Component Reference

### Button

**File:** `frontend/src/components/alignui/button.tsx`
**Figma Node:** `2955-34374`

#### Variants (VERIFIED)
```typescript
variants: {
  variant: ['primary', 'neutral', 'error'],
  mode: ['filled', 'stroke', 'lighter', 'ghost'],
  size: ['medium', 'small', 'xsmall', 'xxsmall']
}
defaultVariants: { variant: 'primary', mode: 'filled', size: 'medium' }
```

#### Exports
```typescript
export { ButtonRoot as Root, ButtonIcon as Icon };
```

#### Token Usage
| State | variant=primary,mode=filled | variant=neutral,mode=stroke |
|-------|-----------------------------|-----------------------------|
| Base | `bg-primary-base text-static-white` | `bg-bg-white-0 text-text-sub-600 ring-stroke-soft-200` |
| Hover | `bg-primary-darker` | `bg-bg-weak-50 text-text-strong-950` |
| Focus | `shadow-button-primary-focus` | `shadow-button-important-focus ring-stroke-strong-950` |
| Disabled | `bg-bg-weak-50 text-text-disabled-300` | Same |

#### Usage Example
```tsx
<Button.Root variant="primary" mode="filled" size="medium">
  <Button.Icon as={RiAddLine} />
  <span>Create Room</span>
</Button.Root>
```

---

### Avatar

**File:** `frontend/src/components/alignui/avatar.tsx`
**Figma Node:** `2906-13402`

#### Variants (VERIFIED)
```typescript
variants: {
  size: ['80', '72', '64', '56', '48', '40', '32', '24', '20'],
  color: ['gray', 'yellow', 'blue', 'sky', 'purple', 'red']
}
defaultVariants: { size: '80', color: 'gray' }
```

#### Exports
```typescript
export {
  AvatarRoot as Root,
  AvatarImage as Image,
  AvatarIndicator as Indicator,
  AvatarStatus as Status,
  AvatarBrandLogo as BrandLogo,
  AvatarNotification as Notification,
};
```

#### Status Variants
```typescript
avatarStatusVariants = {
  status: ['online', 'offline', 'busy', 'away']
}
// Colors: success-base, faded-base, error-base, away-base
```

#### Token Usage
| Size | Root Class |
|------|------------|
| 80 | `size-20 text-title-h5` |
| 48 | `size-12 text-label-lg` |
| 32 | `size-8 text-label-sm` |

#### Usage Example
```tsx
<Avatar.Root size="48" color="blue">
  <Avatar.Image src="/user.jpg" alt="User" />
  <Avatar.Indicator position="bottom">
    <Avatar.Status status="online" />
  </Avatar.Indicator>
</Avatar.Root>
```

---

### Badge

**File:** `frontend/src/components/alignui/badge.tsx`
**Figma Node:** `2939-17953`

#### Variants (VERIFIED)
```typescript
variants: {
  size: ['small', 'medium'],
  variant: ['filled', 'light', 'lighter', 'stroke'],
  color: ['gray', 'blue', 'orange', 'red', 'green', 'yellow', 'purple', 'sky', 'pink', 'teal'],
  disabled: [true, false],
  square: [true, false]
}
defaultVariants: { variant: 'filled', size: 'small', color: 'gray' }
```

#### Exports
```typescript
export { BadgeRoot as Root, BadgeIcon as Icon, BadgeDot as Dot };
```

#### Token Mapping (variant × color)
| Variant | gray | blue | red | green |
|---------|------|------|-----|-------|
| filled | `bg-faded-base text-static-white` | `bg-information-base` | `bg-error-base` | `bg-success-base` |
| light | `bg-faded-light text-faded-dark` | `bg-information-light text-information-dark` | `bg-error-light text-error-dark` | `bg-success-light text-success-dark` |
| lighter | `bg-faded-lighter text-faded-base` | `bg-information-lighter text-information-base` | `bg-error-lighter text-error-base` | `bg-success-lighter text-success-base` |
| stroke | `text-faded-base ring-current` | `text-information-base` | `text-error-base` | `text-success-base` |

#### Usage Example
```tsx
<Badge.Root variant="light" color="green" size="medium">
  <Badge.Dot />
  <span>Active</span>
</Badge.Root>
```

---

### Input

**File:** `frontend/src/components/alignui/input.tsx`
**Figma Node:** `3643-41796`

#### Exports (VERIFY IN CODE)
```bash
grep "export {" frontend/src/components/alignui/input.tsx
```

Expected: `Root`, `Wrapper`, `Input`, `Icon`

#### Token Usage
- Base: `bg-bg-white-0 ring-stroke-soft-200 text-text-strong-950`
- Focus: `ring-stroke-strong-950 shadow-button-important-focus`
- Error: `ring-error-base shadow-button-error-focus`
- Disabled: `bg-bg-weak-50 text-text-disabled-300`

#### Usage Example
```tsx
<Input.Root>
  <Input.Wrapper>
    <Input.Icon as={RiSearchLine} />
    <Input.Input placeholder="Search..." value={value} onChange={...} />
  </Input.Wrapper>
</Input.Root>
```

---

### Select

**File:** `frontend/src/components/alignui/select.tsx`
**Figma Node:** `3211-6627`
**Radix Primitive:** `@radix-ui/react-select`

#### Variants (VERIFIED)
```typescript
variants: {
  size: ['medium', 'small', 'xsmall'],
  variant: ['default', 'compact', 'compactForInput', 'inline'],
  hasError: [true, false]
}
defaultVariants: { variant: 'default', size: 'medium' }
```

#### Exports
```typescript
export {
  SelectRoot as Root,
  SelectContent as Content,
  SelectGroup as Group,
  SelectGroupLabel as GroupLabel,
  SelectItem as Item,
  SelectItemIcon as ItemIcon,
  SelectSeparator as Separator,
  SelectTrigger as Trigger,
  TriggerIcon,
  SelectValue as Value,
};
```

#### Usage Example
```tsx
<Select.Root value={value} onValueChange={setValue}>
  <Select.Trigger>
    <Select.TriggerIcon as={RiCalendarLine} />
    <Select.Value placeholder="Select option" />
  </Select.Trigger>
  <Select.Content>
    <Select.Item value="option1">Option 1</Select.Item>
    <Select.Item value="option2">Option 2</Select.Item>
  </Select.Content>
</Select.Root>
```

---

### Switch

**File:** `frontend/src/components/alignui/switch.tsx`
**Figma Node:** `3677-7838`
**Radix Primitive:** `@radix-ui/react-switch`

#### Exports
```typescript
export { Switch as Root };
```

#### Token Usage
- Unchecked: `bg-bg-soft-200`
- Unchecked Hover: `bg-bg-sub-300`
- Checked: `bg-primary-base`
- Checked Hover: `bg-primary-darker`
- Disabled: `bg-bg-white-0 ring-stroke-soft-200`

#### Usage Example
```tsx
<Switch.Root
  checked={isEnabled}
  onCheckedChange={setIsEnabled}
/>
```

---

### Modal

**File:** `frontend/src/components/alignui/modal.tsx`
**Figma Node:** `3319-16461`
**Radix Primitive:** `@radix-ui/react-dialog`

#### Exports (VERIFY IN CODE)
```bash
grep "export {" frontend/src/components/alignui/modal.tsx
```

Expected: `Root`, `Trigger`, `Content`, `Close`, `Header`, `Body`, `Footer`

#### Token Usage
- Overlay: `bg-overlay`
- Content: `bg-bg-white-0 shadow-regular-md rounded-20`

#### Usage Example
```tsx
<Modal.Root>
  <Modal.Trigger asChild>
    <Button.Root>Open Modal</Button.Root>
  </Modal.Trigger>
  <Modal.Content>
    <Modal.Header>
      <h2>Title</h2>
      <Modal.Close />
    </Modal.Header>
    <Modal.Body>Content</Modal.Body>
    <Modal.Footer>Actions</Modal.Footer>
  </Modal.Content>
</Modal.Root>
```

---

### Drawer

**File:** `frontend/src/components/alignui/drawer.tsx`
**Figma Node:** `4096-39882`
**Radix Primitive:** `@radix-ui/react-dialog`

#### Token Usage
- Panel: `bg-bg-white-0`
- Animation: `slide-in-right`, `slide-out-right`

---

### Divider

**File:** `frontend/src/components/alignui/divider.tsx`
**Figma Node:** `3100-17932`

#### Variants (VERIFY IN CODE)
```typescript
variants: {
  variant: ['line-text', 'line-spacing']
}
```

#### Usage Example
```tsx
<Divider.Root variant="line-spacing" />
```

---

### Label

**File:** `frontend/src/components/alignui/label.tsx`

#### Exports
```typescript
export { Label as Root, LabelAsterisk as Asterisk, LabelSub as Sub };
```

#### Usage Example
```tsx
<Label.Root htmlFor="input">
  <RiUserLine />
  <span>Username</span>
  <Label.Asterisk />
</Label.Root>
```

---

### Textarea

**File:** `frontend/src/components/alignui/textarea.tsx`
**Figma Node:** `3631-1360`

#### Props
```typescript
interface Props {
  simple?: boolean;  // Simplified styling
  hasError?: boolean;
}
```

---

### Alert

**File:** `frontend/src/components/alignui/alert.tsx`
**Figma Node:** `2880-5429`

#### Variants (VERIFY IN CODE)
```bash
grep -A 20 "variants:" frontend/src/components/alignui/alert.tsx
```

Expected variants: `status`, `variant`

---

### Tooltip

**File:** `frontend/src/components/alignui/tooltip.tsx`
**Figma Node:** `3715-41752`
**Radix Primitive:** `@radix-ui/react-tooltip`

#### Token Usage
- Content: `bg-bg-strong-950 text-text-white-0 shadow-tooltip`

---

### Popover

**File:** `frontend/src/components/alignui/popover.tsx`
**Figma Node:** `4431-82035`
**Radix Primitive:** `@radix-ui/react-popover`

---

### Dropdown

**File:** `frontend/src/components/alignui/dropdown.tsx`
**Figma Node:** `166999-144440`
**Radix Primitive:** `@radix-ui/react-dropdown-menu`

---

### Checkbox

**File:** `frontend/src/components/alignui/checkbox.tsx`
**Figma Node:** `3031-3228`
**Radix Primitive:** `@radix-ui/react-checkbox`

---

### Radio

**File:** `frontend/src/components/alignui/radio.tsx`
**Figma Node:** `3401-4760`
**Radix Primitive:** `@radix-ui/react-radio-group`

---

### Pagination

**File:** `frontend/src/components/alignui/pagination.tsx`
**Figma Node:** `3325-20027`

---

### Progress Bar

**File:** `frontend/src/components/alignui/progress-bar.tsx`
**Figma Node:** `3376-287`

---

### Tag

**File:** `frontend/src/components/alignui/tag.tsx`
**Figma Node:** `3571-30133`

---

### Status Badge

**File:** `frontend/src/components/alignui/status-badge.tsx`

---

### Tab Menu

**Files:**
- `frontend/src/components/alignui/tab-menu-horizontal.tsx`
- `frontend/src/components/alignui/tab-menu-vertical.tsx`

**Figma Node:** `3516-12126`

---

### Step Indicators

**Files:**
- `frontend/src/components/alignui/horizontal-stepper.tsx`
- `frontend/src/components/alignui/vertical-stepper.tsx`
- `frontend/src/components/alignui/dot-stepper.tsx`

**Figma Node:** `3508-6266`

---

### Segmented Control

**File:** `frontend/src/components/alignui/segmented-control.tsx`
**Figma Node:** `3688-26806`

---

### Button Variants

**Files:**
- `frontend/src/components/alignui/button-group.tsx`
- `frontend/src/components/alignui/compact-button.tsx`
- `frontend/src/components/alignui/fancy-button.tsx`
- `frontend/src/components/alignui/link-button.tsx`
- `frontend/src/components/alignui/social-button.tsx`

---

### Command Menu

**File:** `frontend/src/components/alignui/command-menu.tsx`
**Figma Node:** `4212-7592`

---

### Table

**File:** `frontend/src/components/alignui/table.tsx`
**Figma Node:** `3525-7648`

---

## Verification Commands

```bash
# List all component files
ls -la frontend/src/components/alignui/

# Get exports from a component
grep "export {" frontend/src/components/alignui/{component}.tsx

# Get variants from a component
grep -A 30 "variants:" frontend/src/components/alignui/{component}.tsx

# Get default variants
grep -A 5 "defaultVariants" frontend/src/components/alignui/{component}.tsx

# Search for specific token usage
grep "bg-" frontend/src/components/alignui/{component}.tsx
grep "text-" frontend/src/components/alignui/{component}.tsx
```

---

## Component Status Legend

| Status | Meaning |
|--------|---------|
| **VERIFIED** | Variants/props confirmed from source code |
| **VERIFY IN CODE** | Needs verification with grep commands |
| **UNKNOWN** | Component structure not confirmed |

---

**Document Status:** Ready for agent consumption
**Maintenance:** Update when new components are added or variants change
