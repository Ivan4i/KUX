# Design System Documentation

## 📋 Содержание

1. [Основы](#основы)
2. [Цветовая палитра](#цветовая-палитра)
3. [Типографика](#типографика)
4. [Spacing & Layout](#spacing--layout)
5. [Breakpoints](#breakpoints)
6. [Grid System](#grid-system)
7. [Z-index Scale](#z-index-scale)
8. [Animation & Motion](#animation--motion)
9. [Accessibility](#accessibility)
10. [Компоненты](#компоненты)
11. [Паттерны](#паттерны)
12. [Состояния](#состояния)
13. [Иконки](#иконки)

---

## Основы

### Принципы дизайна

- **Консистентность**: Единообразие цветов, типографики и компонентов во всех продуктах
- **Читаемость**: Четкая визуальная иерархия с использованием оттенков серого и акцентных цветов
- **Эффективность**: Минималистичный и функциональный подход к дизайну интерфейсов
- **Адаптивность**: Гибкая система, которая работает на всех устройствах и платформах

### Философия

> Простота и ясность превыше всего. Каждый элемент должен иметь четкую цель и работать в гармонии с остальной системой.

---

## Цветовая палитра

### Primary Colors

```css
/* Основной цвет бренда - Blue */
--color-primary: #3384C6;         /* Blue-00 */
--color-primary-hover: #2B6FA8;   /* Darker Blue */
--color-primary-active: #235A8A;  /* Even Darker Blue */
--color-primary-light: #43ABFF;   /* Blue-10 */
--color-primary-dark: #3384C6;    /* Blue-00 */

/* Вторичный цвет - Light Blue */
--color-secondary: #43ABFF;       /* Blue-10 */
--color-secondary-hover: #3699E6; /* Darker */
--color-secondary-active: #2B87CC; /* Even Darker */
--color-secondary-light: #B9E0FF; /* Blue-20 */
--color-secondary-subtle: #E8F5FF; /* Blue-Subtle */
```

### Semantic Colors

```css
/* Success / Trend Up */
--color-success: #00C853;
--color-success-bg: #E8F5E9;
--color-success-border: #81C784;

/* Error / Trend Down */
--color-error: #FF434E;           /* Red */
--color-error-bg: #FFF4F4;        /* Red-Subtle-2 */
--color-error-border: #FFACB1;    /* Red-Light */
--color-error-light: #FFE1E3;     /* Red-Subtle */

/* Warning / Hot */
--color-warning: #FFC107;
--color-warning-bg: #FFF9E6;
--color-warning-border: #FFD54F;

/* Info */
--color-info: #43ABFF;            /* Blue-10 */
--color-info-bg: #E8F5FF;         /* Blue-Subtle */
--color-info-border: #B9E0FF;     /* Blue-20 */
```

### Neutral Colors

```css
/* Text */
--color-text-primary: #000E19;    /* Black */
--color-text-secondary: #333E47;  /* Gray-30 */
--color-text-tertiary: #757D83;   /* Gray-20 */
--color-text-disabled: #B3B7BA;   /* Gray-10 */
--color-text-inverse: #FFFFFF;    /* White */

/* Backgrounds */
--color-bg-primary: #FFFFFF;      /* White */
--color-bg-secondary: #F7F8F8;    /* Gray-BG Subtle */
--color-bg-tertiary: #F2F3F4;     /* Gray-BG */
--color-bg-elevated: #FFFFFF;     /* White */
--color-bg-overlay: rgba(0, 14, 25, 0.5); /* Black with opacity */
--color-bg-card: #F0F4F8;         /* Slate-50 */

/* Stroke / Borders */
--color-border-primary: #DBDDDF;  /* Gray-Line */
--color-border-secondary: #F2F3F4; /* Gray-BG */
--color-border-focus: #43ABFF;    /* Blue-10 */
--color-border-disabled: #B3B7BA; /* Gray-10 */

/* Shades */
--color-gray-50: #F7F8F8;         /* Gray-BG Subtle */
--color-gray-100: #F2F3F4;        /* Gray-BG */
--color-gray-200: #DBDDDF;        /* Gray-Line */
--color-gray-300: #B3B7BA;        /* Gray-10 */
--color-gray-400: #B3B7BA;        /* Gray-10 */
--color-gray-500: #757D83;        /* Gray-20 */
--color-gray-600: #757D83;        /* Gray-20 */
--color-gray-700: #333E47;        /* Gray-30 */
--color-gray-800: #262626;        /* Zinc-800 */
--color-gray-900: #000E19;        /* Black */
--color-black: #000E19;           /* Black */
--color-white: #FFFFFF;           /* White */
```

### Chart Colors

```css
/* Для графиков и визуализации данных */
--color-chart-1: #3384C6;         /* Blue-00 */
--color-chart-2: #43ABFF;         /* Blue-10 */
--color-chart-3: #00C853;         /* Green */
--color-chart-4: #FF434E;         /* Red */
--color-chart-5: #FFC107;         /* Yellow/Warning */
--color-chart-6: #9C27B0;         /* Purple */
--color-chart-7: #FF9800;         /* Orange */
--color-chart-8: #00BCD4;         /* Cyan */
```

### Gradients

```css
/* Градиенты для специальных элементов */
--gradient-primary: linear-gradient(135deg, #3384C6 0%, #43ABFF 100%);
--gradient-secondary: linear-gradient(135deg, #B9E0FF 0%, #E8F5FF 100%);
--gradient-accent: linear-gradient(135deg, #43ABFF 0%, #B9E0FF 100%);
--gradient-overlay: linear-gradient(180deg, rgba(0, 14, 25, 0) 0%, rgba(0, 14, 25, 0.6) 100%);
```

### Brand Icon Colors

```css
/* Цвета для иконок брендов и социальных сетей */
--color-brand-facebook: #1877F2;
--color-brand-twitter: #1DA1F2;
--color-brand-instagram: #E4405F;
--color-brand-linkedin: #0A66C2;
--color-brand-youtube: #FF0000;
--color-brand-github: #181717;
```

---

## Типографика

### Font Family

```css
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-secondary: 'Urbanist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```

### Font Sizes

```css
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-md: 1.125rem;   /* 18px */
--font-size-lg: 1.25rem;    /* 20px */
--font-size-xl: 1.5rem;     /* 24px */
--font-size-2xl: 2rem;      /* 32px */
--font-size-3xl: 2.5rem;    /* 40px */
--font-size-4xl: 3rem;      /* 48px */
--font-size-5xl: 3.75rem;   /* 60px */
--font-size-6xl: 3.85rem;   /* 61.6px - based on leading-[61.60px] */
```

### Font Weights

```css
--font-weight-thin: 100;
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
--font-weight-extrabold: 800;
--font-weight-black: 900;
```

### Line Heights

```css
--line-height-tight: 1.25;      /* 125% */
--line-height-snug: 1.375;      /* 137.5% */
--line-height-normal: 1.5;      /* 150% */
--line-height-relaxed: 1.625;   /* 162.5% */
--line-height-loose: 2;         /* 200% */
```

### Text Styles

#### Headings

- **H1**: Font: Urbanist, Size: 60px (3.75rem), Weight: 500 (Medium), Line Height: 61.6px, Color: #000E19
- **H2**: Font: Urbanist, Size: 48px (3rem), Weight: 500 (Medium), Line Height: 1.2, Color: #000E19
- **H3**: Font: Urbanist, Size: 40px (2.5rem), Weight: 500 (Medium), Line Height: 1.2, Color: #000E19
- **H4**: Font: Urbanist, Size: 32px (2rem), Weight: 500 (Medium), Line Height: 1.3, Color: #000E19
- **H5**: Font: Urbanist, Size: 24px (1.5rem), Weight: 500 (Medium), Line Height: 1.4, Color: #000E19
- **H6**: Font: Urbanist, Size: 20px (1.25rem), Weight: 500 (Medium), Line Height: 1.4, Color: #000E19

#### Body Text

- **Body Large**: Font: Inter, Size: 18px (1.125rem), Weight: 400 (Normal), Line Height: 1.5, Color: #000E19
- **Body**: Font: Inter, Size: 16px (1rem), Weight: 400 (Normal), Line Height: 1 (16px), Color: #000E19
- **Body Small**: Font: Inter, Size: 14px (0.875rem), Weight: 400 (Normal), Line Height: 1.4, Color: #757D83
- **Caption**: Font: Inter, Size: 12px (0.75rem), Weight: 400 (Normal), Line Height: 0.75 (12px), Color: #757D83

#### Tracking (Letter Spacing)

```css
--letter-spacing-tight: -0.02em;   /* -2% */
--letter-spacing-normal: 0;        /* 0 */
--letter-spacing-wide: 0.02em;     /* 2% */
--letter-spacing-wider: 0.05em;    /* 5% */
```

---

## Spacing & Layout

### Spacing Scale

```css
--space-0: 0;           /* 0px */
--space-1: 0.25rem;     /* 4px */
--space-2: 0.5rem;      /* 8px */
--space-2-5: 0.625rem;  /* 10px - gap-2.5 */
--space-3: 0.75rem;     /* 12px */
--space-4: 1rem;        /* 16px */
--space-5: 1.25rem;     /* 20px */
--space-6: 1.5rem;      /* 24px */
--space-7: 1.75rem;     /* 28px - gap-7 */
--space-8: 2rem;        /* 32px */
--space-10: 2.5rem;     /* 40px */
--space-12: 3rem;       /* 48px - p-12, pt-12, pb-16=64px */
--space-14: 3.5rem;     /* 56px - gap-14 */
--space-16: 4rem;       /* 64px - p-16 */
--space-20: 5rem;       /* 80px */
--space-24: 6rem;       /* 96px */
--space-52: 13rem;      /* 208px - gap-52 */
```

### Border Radius

```css
--radius-none: 0;
--radius-sm: 0.25rem;   /* 4px */
--radius-base: 0.5rem;  /* 8px */
--radius-md: 0.625rem;  /* 10px */
--radius-lg: 0.75rem;   /* 12px - rounded-lg */
--radius-xl: 1rem;      /* 16px - rounded-xl */
--radius-2xl: 1.5rem;   /* 24px - rounded-2xl */
--radius-3xl: 3.75rem;  /* 60px - rounded-tl-[60px] */
--radius-full: 9999px;
```

### Shadows

#### Card Shadows

```css
--shadow-xs: 0 1px 2px 0 rgba(0, 14, 25, 0.05);
--shadow-sm: 0 1px 3px 0 rgba(0, 14, 25, 0.1), 0 1px 2px -1px rgba(0, 14, 25, 0.1);
--shadow-base: 0 4px 6px -1px rgba(0, 14, 25, 0.1), 0 2px 4px -2px rgba(0, 14, 25, 0.1);
--shadow-md: 0 10px 15px -3px rgba(0, 14, 25, 0.1), 0 4px 6px -4px rgba(0, 14, 25, 0.1);
--shadow-lg: 0 20px 25px -5px rgba(0, 14, 25, 0.1), 0 8px 10px -6px rgba(0, 14, 25, 0.1);
--shadow-xl: 0 25px 50px -12px rgba(0, 14, 25, 0.25);
```

#### Button Shadows

```css
--shadow-button: 0 2px 4px 0 rgba(0, 14, 25, 0.1);
--shadow-button-hover: 0 4px 8px 0 rgba(0, 14, 25, 0.15);
--shadow-button-active: 0 1px 2px 0 rgba(0, 14, 25, 0.1);
```

#### Hover Shadows

```css
--shadow-hover-sm: 0 4px 8px 0 rgba(0, 14, 25, 0.12);
--shadow-hover-md: 0 8px 16px 0 rgba(0, 14, 25, 0.15);
--shadow-hover-lg: 0 12px 24px 0 rgba(0, 14, 25, 0.18);
```

### Borders

#### Border Width

```css
--border-width-0: 0;
--border-width-1: 1px;
--border-width-2: 2px;
--border-width-4: 4px;
```

#### Border Offset

```css
--border-offset-0: 0;
--border-offset-1: 1px;
--border-offset-2: 2px;
```

### Opacity Scale

```css
--opacity-0: 0;         /* 0% */
--opacity-5: 0.05;      /* 5% */
--opacity-10: 0.1;      /* 10% */
--opacity-20: 0.2;      /* 20% */
--opacity-30: 0.3;      /* 30% */
--opacity-40: 0.4;      /* 40% */
--opacity-50: 0.5;      /* 50% */
--opacity-60: 0.6;      /* 60% */
--opacity-70: 0.7;      /* 70% */
--opacity-80: 0.8;      /* 80% */
--opacity-90: 0.9;      /* 90% */
--opacity-100: 1;       /* 100% */
```

---

## Breakpoints

Responsive breakpoints для адаптивного дизайна на всех устройствах.

### Breakpoint Scale

```css
--breakpoint-xs: 320px;   /* Mobile Small */
--breakpoint-sm: 480px;   /* Mobile Large */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop Small */
--breakpoint-xl: 1440px;  /* Desktop Large */
--breakpoint-2xl: 1920px; /* Desktop XL */
```

### Device Ranges

| Breakpoint | Range | Devices | Layout |
|------------|-------|---------|--------|
| **XS** | 320px - 479px | Mobile phones (portrait) | Single column, stacked layout |
| **SM** | 480px - 767px | Mobile phones (landscape), small tablets | Single column, compact spacing |
| **MD** | 768px - 1023px | Tablets (portrait), small laptops | 2 columns, medium spacing |
| **LG** | 1024px - 1439px | Tablets (landscape), laptops | 3-4 columns, comfortable spacing |
| **XL** | 1440px - 1919px | Desktop monitors | Full layout, generous spacing |
| **2XL** | 1920px+ | Large desktop monitors, 4K | Max-width containers, extra spacing |

### Media Queries

```css
/* Mobile First Approach */
@media (min-width: 480px) {  /* SM */ }
@media (min-width: 768px) {  /* MD */ }
@media (min-width: 1024px) { /* LG */ }
@media (min-width: 1440px) { /* XL */ }
@media (min-width: 1920px) { /* 2XL */ }

/* Desktop First Approach */
@media (max-width: 1919px) { /* XL and below */ }
@media (max-width: 1439px) { /* LG and below */ }
@media (max-width: 1023px) { /* MD and below */ }
@media (max-width: 767px) {  /* SM and below */ }
@media (max-width: 479px) {  /* XS only */ }
```

### Responsive Design Guidelines

**Container Max Widths:**
- **XS/SM**: 100% (no max-width)
- **MD**: 768px
- **LG**: 1024px
- **XL**: 1280px
- **2XL**: 1536px

**Padding/Margin Scale by Breakpoint:**
- **XS/SM**: 16px (1rem)
- **MD**: 24px (1.5rem)
- **LG**: 32px (2rem)
- **XL**: 40px (2.5rem)

**Typography Scale Adjustment:**
- **Mobile (XS/SM)**: Base font 14px-16px
- **Tablet (MD)**: Base font 16px
- **Desktop (LG+)**: Base font 16px-18px

**Component Behavior:**
- **Tables**: Switch to card view on mobile (< 768px)
- **Navigation**: Hamburger menu on mobile/tablet (< 1024px)
- **Sidebars**: Collapse or hide on mobile (< 768px)
- **Grids**: 1 col (XS), 2 cols (SM/MD), 3-4 cols (LG+)
- **Modals**: Full screen on mobile (< 768px), centered on desktop

---

## Grid System

Flexible grid system для создания responsive layouts.

### Grid Container

```css
.grid-container {
  display: grid;
  width: 100%;
  max-width: var(--breakpoint-xl); /* 1440px */
  margin: 0 auto;
  padding: 0 var(--space-4); /* 16px */
}
```

### Grid Columns

**12-Column Grid:**
```css
--grid-columns: 12;
--grid-gap: 24px;  /* Default gap between columns */

/* Column Widths */
.col-1  { grid-column: span 1; }   /* 8.33% */
.col-2  { grid-column: span 2; }   /* 16.66% */
.col-3  { grid-column: span 3; }   /* 25% */
.col-4  { grid-column: span 4; }   /* 33.33% */
.col-6  { grid-column: span 6; }   /* 50% */
.col-8  { grid-column: span 8; }   /* 66.66% */
.col-12 { grid-column: span 12; }  /* 100% */
```

### Grid Gap Scale

```css
--grid-gap-none: 0;
--grid-gap-xs: 8px;
--grid-gap-sm: 16px;
--grid-gap-base: 24px;  /* Default */
--grid-gap-md: 32px;
--grid-gap-lg: 40px;
--grid-gap-xl: 48px;
```

### Responsive Grid

**Mobile (< 768px):**
```css
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}
```

**Tablet (768px - 1023px):**
```css
.grid {
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
```

**Desktop (1024px+):**
```css
.grid {
  grid-template-columns: repeat(3, 1fr); /* or repeat(4, 1fr) */
  gap: 32px;
}
```

### Layout Patterns

**Sidebar + Content:**
```css
.layout-sidebar {
  display: grid;
  grid-template-columns: 240px 1fr; /* Fixed sidebar */
  gap: 0;
}

@media (max-width: 1023px) {
  .layout-sidebar {
    grid-template-columns: 1fr; /* Stack on mobile */
  }
}
```

**Dashboard Grid:**
```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}
```

**Holy Grail Layout:**
```css
.holy-grail {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar content aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}
```

### Container Utilities

**Max-Width Containers:**
```css
.container-sm  { max-width: 640px; }
.container-md  { max-width: 768px; }
.container-lg  { max-width: 1024px; }
.container-xl  { max-width: 1280px; }
.container-2xl { max-width: 1536px; }
```

---

## Z-index Scale

Hierarchical z-index system для управления слоями интерфейса.

### Z-index Values

```css
--z-base: 0;           /* Normal flow */
--z-dropdown: 100;     /* Dropdowns, popovers */
--z-sticky: 200;       /* Sticky headers, floating buttons */
--z-fixed: 300;        /* Fixed navigation bars */
--z-modal-backdrop: 400; /* Modal backdrops */
--z-modal: 500;        /* Modals, dialogs */
--z-popover: 600;      /* Popovers above modals */
--z-tooltip: 700;      /* Tooltips */
--z-notification: 800; /* Toast notifications */
--z-max: 999;          /* Highest priority (rare use) */
```

### Z-index Hierarchy

| Layer | Z-index | Elements | Usage |
|-------|---------|----------|-------|
| **Base** | 0 | Normal content, cards | Default document flow |
| **Dropdown** | 100 | Select dropdowns, context menus | Above normal content |
| **Sticky** | 200 | Sticky headers, FAB buttons | Stays above scrolling content |
| **Fixed** | 300 | Navigation bars, toolbars | Fixed position elements |
| **Modal Backdrop** | 400 | Modal overlays, drawers | Blocks interaction with content |
| **Modal** | 500 | Modal dialogs, side panels | Above backdrop |
| **Popover** | 600 | Popovers, date pickers | Above modals if needed |
| **Tooltip** | 700 | Tooltips, help text | Always visible when triggered |
| **Notification** | 800 | Toast messages, alerts | Highest priority messages |
| **Max** | 999 | Emergency overlays | Rare use, debugging only |

### Usage Guidelines

**Best Practices:**
- Use defined variables, never hardcode z-index values
- Only use z-index when elements actually overlap
- Keep components within their assigned layer range
- Avoid z-index wars (competing high values)

**Component Z-index:**
```css
/* Good */
.dropdown {
  z-index: var(--z-dropdown);
}

.modal {
  z-index: var(--z-modal);
}

/* Bad */
.dropdown {
  z-index: 999999; /* Don't do this */
}
```

**Stacking Context:**
- Modals create new stacking context (isolate from parent z-index)
- Fixed/absolute positioned elements with z-index create stacking context
- Transform, filter, opacity < 1 create stacking context

---

## Animation & Motion

Animation system для создания плавных и согласованных переходов.

### Animation Principles

- **Purposeful**: Анимации должны улучшать UX, а не отвлекать
- **Consistent**: Единообразие в timing и easing functions
- **Performance**: Используйте transform и opacity для лучшей производительности
- **Subtle**: Анимации должны быть заметными, но не навязчивыми

### Duration Scale

```css
--duration-instant: 50ms;    /* Instant feedback */
--duration-fast: 100ms;      /* Quick transitions */
--duration-base: 150ms;      /* Default transitions */
--duration-medium: 200ms;    /* Moderate transitions */
--duration-slow: 300ms;      /* Slow, noticeable transitions */
--duration-slower: 500ms;    /* Very slow transitions */
--duration-animation: 1000ms; /* Animations, loaders */
```

### Duration Usage

| Duration | Use Case | Examples |
|----------|----------|----------|
| **50ms** | Instant feedback | Button press, checkbox toggle |
| **100ms** | Quick state change | Hover effects, focus rings |
| **150ms** | Default transition | Background color, border changes |
| **200ms** | Smooth movement | Dropdown expand, tooltip appear |
| **300ms** | Noticeable change | Sidebar collapse, panel slide |
| **500ms** | Deliberate animation | Modal fade in, drawer slide |
| **1000ms+** | Loaders, complex animations | Skeleton shimmer, progress bars |

### Easing Functions

```css
--ease-linear: linear;
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-smooth: cubic-bezier(0.25, 0.1, 0.25, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
--ease-elastic: cubic-bezier(0.5, 1.5, 0.5, 1);
```

### Easing Usage

| Easing | Use Case | Feel |
|--------|----------|------|
| **Linear** | Loaders, continuous animations | Constant speed |
| **Ease-in** | Elements disappearing | Starts slow, accelerates |
| **Ease-out** | Elements appearing | Starts fast, decelerates |
| **Ease-in-out** | Movement between states | Smooth acceleration & deceleration |
| **Smooth** | Subtle transitions | Natural, polished |
| **Bounce** | Playful interactions | Bouncy, energetic |
| **Elastic** | Attention-grabbing | Springy, exaggerated |

### Transition Properties

**Commonly Animated Properties:**
```css
/* ✅ Good for performance (GPU accelerated) */
transition: transform 150ms ease-out;
transition: opacity 150ms ease-out;

/* ⚠️ OK, but less performant */
transition: background-color 150ms ease-out;
transition: color 150ms ease-out;
transition: border-color 150ms ease-out;

/* ❌ Avoid (causes layout reflow) */
transition: width 150ms ease-out;
transition: height 150ms ease-out;
transition: padding 150ms ease-out;
```

### Animation Presets

**Fade In:**
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in {
  animation: fadeIn 200ms ease-out;
}
```

**Slide In (from right):**
```css
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.slide-in-right {
  animation: slideInRight 300ms ease-out;
}
```

**Scale In:**
```css
@keyframes scaleIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.scale-in {
  animation: scaleIn 200ms ease-out;
}
```

**Shimmer (Loading):**
```css
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.shimmer {
  animation: shimmer 1.5s ease-in-out infinite;
  background: linear-gradient(90deg,
    #F2F3F4 0%,
    #E5E5E5 50%,
    #F2F3F4 100%
  );
  background-size: 1000px 100%;
}
```

**Spin (Loading):**
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spin {
  animation: spin 800ms linear infinite;
}
```

**Pulse:**
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}
```

### Component-Specific Animations

**Buttons:**
```css
.button {
  transition: all 150ms ease-out;
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-button-hover);
}

.button:active {
  transform: scale(0.98);
  transition-duration: 50ms;
}
```

**Modals:**
```css
.modal-backdrop {
  transition: opacity 300ms ease-out;
}

.modal-content {
  transition: all 300ms ease-out;
  animation: scaleIn 300ms ease-out;
}
```

**Dropdowns:**
```css
.dropdown {
  transition: all 200ms ease-out;
  transform-origin: top;
}

.dropdown.open {
  transform: scaleY(1);
  opacity: 1;
}

.dropdown.closed {
  transform: scaleY(0);
  opacity: 0;
}
```

**Tooltips:**
```css
.tooltip {
  transition: opacity 100ms ease-out;
}

.tooltip.visible {
  opacity: 1;
}
```

### Reduced Motion

**Respect User Preferences:**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Performance Guidelines

**DO:**
- Use transform and opacity for animations
- Use will-change for complex animations (sparingly)
- Animate on GPU-accelerated properties
- Keep animations under 300ms for interactions
- Use requestAnimationFrame for JS animations

**DON'T:**
- Animate width, height, padding, margin
- Overuse will-change (wastes memory)
- Chain multiple slow animations
- Animate more than 3-4 properties simultaneously
- Use JavaScript when CSS can do it

---

## Accessibility

Руководство по созданию доступных интерфейсов для всех пользователей.

### WCAG 2.1 Compliance

**Target Level**: WCAG 2.1 Level AA

**Key Requirements:**
- Color contrast ratio: 4.5:1 (normal text), 3:1 (large text)
- All interactive elements keyboard accessible
- Focus indicators clearly visible
- Text resizable up to 200% without loss of functionality
- No content flashing more than 3 times per second

### Color Contrast

**Text Contrast Ratios:**

| Background | Text Color | Contrast | Pass/Fail |
|------------|------------|----------|-----------|
| White (#FFFFFF) | Zinc-800 (#27272A) | 15.8:1 | ✅ AAA |
| White (#FFFFFF) | Neutral-500 (#737373) | 4.6:1 | ✅ AA |
| Teal-900 (#164E3F) | White (#FFFFFF) | 9.2:1 | ✅ AAA |
| Teal-900 (#164E3F) | Lime-200 (#ECFCCB) | 8.1:1 | ✅ AAA |
| Stone-100 (#F5F5F4) | Zinc-800 (#27272A) | 14.2:1 | ✅ AAA |
| Blue-500 (#3384C6) | White (#FFFFFF) | 5.1:1 | ✅ AA |

**Ensure Sufficient Contrast:**
- Body text (16px): minimum 4.5:1
- Large text (18px+, 14px bold+): minimum 3:1
- UI components (buttons, inputs): minimum 3:1
- Graphical objects (icons, charts): minimum 3:1

### Keyboard Navigation

**Tab Order:**
- Logical tab order following visual flow
- All interactive elements focusable
- Skip links for main content
- Focus traps in modals and dropdowns

**Keyboard Shortcuts:**
- `Tab` / `Shift+Tab`: Navigate between elements
- `Enter` / `Space`: Activate buttons, checkboxes
- `Escape`: Close modals, dropdowns, tooltips
- `Arrow keys`: Navigate lists, menus, tabs
- `Home` / `End`: Jump to first/last item

**Focus Indicators:**
```css
:focus-visible {
  outline: 3px solid #43ABFF;
  outline-offset: 2px;
  border-radius: 4px;
}

/* High contrast mode */
@media (prefers-contrast: high) {
  :focus-visible {
    outline: 4px solid currentColor;
  }
}
```

### ARIA Attributes

**Landmarks:**
```html
<header role="banner">
<nav role="navigation" aria-label="Main navigation">
<main role="main">
<aside role="complementary">
<footer role="contentinfo">
```

**Widgets:**
```html
<!-- Button -->
<button aria-label="Close dialog" aria-pressed="false">

<!-- Toggle Switch -->
<button role="switch" aria-checked="true" aria-label="Enable notifications">

<!-- Checkbox -->
<input type="checkbox" aria-checked="true" aria-labelledby="label-id">

<!-- Modal -->
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">

<!-- Dropdown -->
<button aria-haspopup="true" aria-expanded="false">
<ul role="menu">
  <li role="menuitem">
```

**Live Regions:**
```html
<!-- Notifications -->
<div role="alert" aria-live="assertive">Error: Form submission failed</div>

<!-- Status updates -->
<div role="status" aria-live="polite">Loading...</div>

<!-- Dynamic content -->
<div aria-live="polite" aria-atomic="true">3 items in cart</div>
```

### Screen Reader Support

**Alternative Text:**
- All images have meaningful alt text
- Decorative images use alt=""
- Icons with meaning have aria-label
- Link text is descriptive (not "click here")

**Forms:**
```html
<!-- Label association -->
<label for="email">Email Address</label>
<input id="email" type="email" required aria-required="true">

<!-- Error messages -->
<input aria-invalid="true" aria-describedby="error-email">
<span id="error-email" role="alert">Please enter a valid email</span>

<!-- Help text -->
<input aria-describedby="help-password">
<span id="help-password">Password must be at least 8 characters</span>
```

**Tables:**
```html
<table role="table">
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Transaction 1</td>
      <td>$100</td>
    </tr>
  </tbody>
</table>
```

### Touch Targets

**Minimum Size:**
- Mobile: 44×44px (iOS), 48×48px (Android)
- Desktop: 32×32px minimum
- Spacing: 8px minimum between targets

**Interactive Elements:**
- Buttons: 32×32px minimum (desktop), 44×44px (mobile)
- Checkboxes: 16×16px visual, 44×44px touch area
- Links: 16px font minimum, generous padding
- Form inputs: 40px height minimum (mobile)

### Color Blindness

**Don't Rely on Color Alone:**
- Use icons + color for status (not just green/red)
- Add patterns/textures to charts
- Underline links in body text
- Use labels with color-coded items

**Color Blind Safe Palette:**
- Use high contrast combinations
- Avoid red/green only distinctions
- Test with color blindness simulators
- Provide alternative indicators (icons, text, patterns)

### Motion & Vestibular Disorders

**Reduced Motion:**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

**Guidelines:**
- Avoid parallax scrolling
- No auto-playing videos without controls
- Provide pause/stop controls for animations
- Limit motion to <300ms or make optional

### Semantic HTML

**Use Proper Elements:**
```html
<!-- ✅ Good -->
<button>Submit</button>
<a href="/page">Link</a>
<input type="checkbox">
<select>...</select>

<!-- ❌ Bad -->
<div onclick="...">Submit</div>
<div onclick="...">Link</div>
<div class="checkbox">...</div>
<div class="select">...</div>
```

### Testing Checklist

**Keyboard Navigation:**
- [ ] All interactive elements reachable via Tab
- [ ] Focus order is logical
- [ ] Focus indicators clearly visible
- [ ] No keyboard traps
- [ ] Escape closes modals/dropdowns

**Screen Readers:**
- [ ] Test with NVDA (Windows) or VoiceOver (Mac/iOS)
- [ ] All content announced correctly
- [ ] Form labels associated properly
- [ ] Error messages announced
- [ ] Dynamic content updates announced

**Visual:**
- [ ] Text contrast meets WCAG AA
- [ ] Content readable at 200% zoom
- [ ] No information conveyed by color alone
- [ ] Touch targets minimum 44×44px (mobile)

**Tools:**
- **axe DevTools**: Browser extension for accessibility testing
- **WAVE**: Web accessibility evaluation tool
- **Lighthouse**: Chrome DevTools accessibility audit
- **Color Contrast Analyzer**: Check contrast ratios
- **Screen Readers**: NVDA, JAWS, VoiceOver

---

## Компоненты

### 1. Cards

#### Blog/Article Cards

**Horizontal Card with Image (Large):**
- **Container**: Width 384px (w-96), Padding 12px (p-3), Background #F5F5F4 (Stone-100), Border Radius 16px (rounded-2xl)
- **Layout**: Flex row, Gap 12px (gap-3)
- **Image**: 112px × 112px (w-28 h-28), Border Radius 16px (rounded-2xl), Background #E5E5E5 (Neutral-200)
- **Content Padding**: 4px horizontal (px-1)
- **Category**: Color #164E3F (Teal-900), Font Urbanist 12px Medium, Line Height 16px
- **Date**: Color #737373 (Neutral-500), Font Urbanist 12px Medium, Separator: 3px dot #E5E5E5
- **Title**: Color #262626 (Zinc-800), Font Urbanist 18px Semibold, Line Height 20px, line-clamp-1
- **Description**: Color #737373 (Neutral-500), Font Urbanist 12px Normal, Line Height 20px, line-clamp-2
- **Avatar**: 20px (w-5 h-5), Background #ECFCCB (Lime-200), Border Radius 20px (rounded-[20px])
- **Author**: Color #262626 (Zinc-800), Font Urbanist 12px Medium

**Horizontal Card with Image (Medium):**
- **Container**: Width 320px (w-80), Gap 14px (gap-3.5)
- **Image**: 96px × 96px (w-24 h-24), Border Radius 16px (rounded-2xl)
- **Title**: Font Urbanist 18px Semibold, Line Height 20px, line-clamp-2

**Vertical Card with Image (Medium):**
- **Container**: Width 256px (w-64), Flex column, Gap 14px (gap-3.5)
- **Image**: Height 160px (h-40), Full width, Border Radius 16px (rounded-2xl)
- **Content Padding**: 4px horizontal (px-1)
- **Title**: Font Urbanist 20px Bold, Line Height 24px
- **Description**: Font Urbanist 12px Normal, Line Height 20px

**Simple Horizontal Card:**
- **Container**: Width 224px (w-56), Flex row, Gap 12px (gap-3)
- **Icon**: 10px × 10px square, Background #164E3F (Teal-900), Border Radius 3px (rounded-[3px])
- **Title**: Font Urbanist 14px Semibold
- **Amount**: Color #737373 (Neutral-500), Font Urbanist 14px Semibold
- **Badge**: Padding 6px (p-1.5), Background #F5F5F4 (Stone-100), Border Radius 6px (rounded-md)

---

#### Stat Cards

**Stat Card with Icon (Horizontal):**
- **Container**: Width 384px (w-96), Padding 16px (p-4), Background #FAFAFA (Neutral-50), Border 1px #FFFFFF (Neutral-50), Border Radius 16px (rounded-2xl)
- **Layout**: Space between
- **Left Section**:
  - Label: Font Urbanist 14px Medium, Color #262626 (Zinc-800)
  - Value: Font Urbanist 24px Bold, Color #164E3F (Teal-900)
  - Badge: Background #ECFCCB (Lime-200), Padding 5px 2px (px-[5px] py-0.5), Border Radius 16px (rounded-2xl)
    - Icon: 12px (w-3 h-3)
    - Text: Font Urbanist 10px Semibold, Color #164E3F (Teal-900)
- **Icon Container**: Padding 12px (p-3), Background #FAFAFA (Neutral-50), Border Radius 9999px (rounded-full)
  - Icon: 32px (w-8 h-8), Color #164E3F (Teal-900)

**Stat Card with Icon (Simple):**
- **Container**: Width 288px (w-72), Padding 16px (p-4), Background #FAFAFA (Neutral-50), Border 1px #E5E5E5 (Neutral-200), Border Radius 16px (rounded-2xl)
- **Icon Container**: Padding 8px (p-2), Background #F5F5F4 (Stone-100), Border Radius 8px (rounded-lg)
  - Icon: 14px (w-3.5 h-3.5), Color #164E3F (Teal-900)
- **Label**: Font Urbanist 14px Medium
- **Value**: Font Urbanist 24px Bold, Color #164E3F (Teal-900)
- **Change Badge**: Same as above
- **Comparison Text**: Font Urbanist 12px, Mixed weights

---

#### Bank/Credit Cards

**Credit Card (Dark):**
- **Container**: Width 256px (w-64), Padding 16px (p-4), Background #164E3F (Teal-900), Border Radius 16px (rounded-2xl)
- **Layout**: Flex column, Gap 24px (gap-6)
- **Card Name**: Font Urbanist 10px Semibold, Color #F5F5F4 (Stone-100)
- **Logo Area**: Mastercard circles - 24px each (w-6 h-6), Colors: #ECFCCB (Lime-200) opacity 80%, #F5F5F4 (Stone-100)
- **Balance**: Font Urbanist 20px Bold, Color #FAFAFA (Neutral-50)
- **Card Type**: Font Urbanist 14px Semibold, Color #F5F5F4 (Stone-100)
- **Card Number**: Font Urbanist 12px Semibold, Color #FAFAFA (Neutral-50)
- **Labels**: Font Urbanist 10px Normal, Color #F5F5F4 (Stone-100)
- **Values (EXP/CVV)**: Font Urbanist 12px Semibold, Color #FAFAFA (Neutral-50)

**Credit Card (Light):**
- Same layout, different colors:
- **Background**: #FAFAFA (Neutral-50)
- **Text**: #262626 (Zinc-800)
- **Labels**: #737373 (Neutral-500)
- **Logo**: Teal-900 opacity 30%, Lime-200 opacity 80%

---

#### Progress/Goal Cards

**Goal Card with Icon (Compact):**
- **Container**: Width 256px (w-64), Padding 14px (p-3.5), Border 1px #E5E5E5 (Neutral-200), Border Radius 12px (rounded-xl)
- **Header**: Space between
  - Icon: Padding 6px (p-1.5), Background #F5F5F4 (Stone-100), Border Radius 8px (rounded-lg), Icon 16px (w-4 h-4)
  - Title: Font Urbanist 12px Medium
  - Menu icon: 16px (w-4 h-4), Transparent button
- **Progress Bar**:
  - Height: 8px (h-2)
  - Border Radius: 8px (rounded-lg)
  - Fill: Background #164E3F (Teal-900)
  - Remaining: Background #ECFCCB (Lime-200)
- **Info Row**:
  - Current: Font Urbanist 10px Semibold, Color #262626 (Zinc-800)
  - Percentage: Font Urbanist 10px Semibold, Color #737373 (Neutral-500)
  - Target: Font Urbanist 10px Normal, Mixed colors

**Goal Card (Simple List Item):**
- **Container**: Width 256px (w-64), Padding vertical 14px (py-3.5), Border bottom 1px #E5E5E5 (Neutral-200)
- **Title**: Font Urbanist 12px Semibold
- **Progress Bar**: Height 8px (h-2), Border Radius 4px (rounded)
- **Values**: Font Urbanist 10px Semibold

**Goal Card (Large):**
- **Container**: Width 320px (w-80), Padding 14px (p-3.5), Border 1px #E5E5E5, Border Radius 12px (rounded-xl)
- **Icon**: Padding 10px (p-2.5), Background #F5F5F4, Border Radius 20px (rounded-[20px]), Icon 20px (w-5 h-5)
- **Title**: Font Urbanist 16px Semibold
- **Values**: Font Urbanist 14px Semibold/Normal
- **Status**: Font Urbanist 14px Semibold, Color #164E3F (Teal-900)
- **Progress**: Font Urbanist 16px Semibold
- **Progress Bar**: Height 12px (h-3), Border Radius 4px (rounded)

---

#### Feature/Metric Cards

**Feature Card with Icon (Vertical):**
- **Container**: Width 176px (w-44), Padding 16px (p-4), Border 1px #E5E5E5 (Neutral-200), Border Radius 16px (rounded-2xl)
- **Layout**: Flex column, Gap 28px (gap-7)
- **Icon**: Padding 8px (p-2), Background #F5F5F4 (Stone-100), Border Radius 8px (rounded-lg), Icon 20px (w-5 h-5)
- **Badge**: Padding 4px horizontal 1px vertical (px-1 py-px), Background #ECFCCB (Lime-200), Border Radius 16px (rounded-2xl)
  - Icon: 10px (w-2.5 h-2.5)
  - Text: Font Urbanist 8px Medium
- **Value**: Font Urbanist 24px Bold, Color #262626 (Zinc-800)
- **Label**: Font Urbanist 12px Normal, Color #262626 (Zinc-800)

**Feature Card (Horizontal - Large):**
- **Container**: Width 320px (w-80), Padding 16px (p-4), Border 1px #E5E5E5, Border Radius 16px (rounded-2xl)
- **Icon**: Padding 12px (p-3), Background #F5F5F4, Border Radius 8px (rounded-lg), Icon 28px (w-7 h-7)
- **Value**: Font Urbanist 24px Bold
- **Label**: Font Urbanist 12px Normal

---

#### Promo/Offer Cards

**Promo Card (Vertical):**
- **Container**: Width 288px (w-72), Padding 12px (p-3), Border 1px #E5E5E5 (Neutral-200), Border Radius 16px (rounded-2xl)
- **Image**: Height 144px (h-36), Full width, Border Radius 12px (rounded-xl), Background #E5E5E5
- **Content**: Padding horizontal 4px (px-1), Gap 10px (gap-2.5)
- **Title**: Font Urbanist 18px Semibold, Line Height 20px
- **Description**: Font Urbanist 12px Normal, Line Height 20px, line-clamp-2
- **Date Label**: Font Urbanist 12px Medium, Color #737373 (Neutral-500)
- **Date**: Font Urbanist 12px Medium, Color #262626 (Zinc-800)

**Promo Card (Horizontal):**
- **Container**: Width 320px (w-80), Gap 12px (gap-3)
- **Image**: 96px × 96px (w-24 h-24), Border Radius 12px (rounded-xl)
- **Title**: Font Urbanist 16px Semibold, Line Height 20px
- **Description**: Font Urbanist 14px Normal, Line Height 20px, line-clamp-2

---

#### Content Cards

**Content Card (Simple):**
- **Container**: Width 208px (w-52), Flex column, Gap 12px (gap-3)
- **Image**: Height 128px (h-32), Full width, Border Radius 16px (rounded-2xl), Background #E5E5E5
- **Content**: Padding horizontal 6px (px-1.5), Gap 6px (gap-1.5)
- **Category**: Font Urbanist 12px Medium, Color #164E3F (Teal-900)
- **Title**: Font Urbanist 16px Semibold, Line Height 20px

**Content Card (Large):**
- **Container**: Width 320px (w-80), Gap 12px (gap-3)
- **Image**: Height 192px (h-48), Border Radius 16px (rounded-2xl)
- **Title**: Font Urbanist 18px Semibold, Line Height 20px

**Content Card with Meta:**
- **Container**: Width 208px (w-52) or 320px (w-80), Gap 14px (gap-3.5)
- **Image**: Height 128px (h-32) or 208px (h-52), Border Radius 16px (rounded-2xl)
- **Category + Date**: Separator - 3px dot (w-[3px] h-[3px]), Background #E5E5E5 (Neutral-200), Border Radius full
- **Title**: Font Urbanist 18px Semibold, Line Height 20px

---

#### Common Card Elements

**Avatar:**
- **Size**: 20px (w-5 h-5)
- **Border Radius**: 20px (rounded-[20px])
- **Background**: #ECFCCB (Lime-200) or image

**Badge (Change indicator):**
- **Padding**: 5px 2px (px-[5px] py-0.5) or 4px 1px (px-1 py-px)
- **Border Radius**: 16px (rounded-2xl)
- **Background**: #ECFCCB (Lime-200)
- **Icon**: 12px (w-3 h-3) or 10px (w-2.5 h-2.5), Color #164E3F (Teal-900)
- **Text**: Font Urbanist 10px or 8px Semibold/Medium, Color #164E3F (Teal-900)

**Separator Dot:**
- **Size**: 3px × 3px (w-[3px] h-[3px])
- **Background**: #E5E5E5 (Neutral-200)
- **Border Radius**: Full (rounded-full)

**Progress Bar:**
- **Container**: Full width, Height 8px or 12px, Border Radius matching
- **Fill**: Background #164E3F (Teal-900)
- **Empty**: Background #ECFCCB (Lime-200)

---

### 2. Buttons

#### Button Sizes

**Small:**
- **Height**: 20px (h-5)
- **Padding**: 6px 10px (px-2.5 py-1.5)
- **Font**: Urbanist, 10px, Weight 500 (Medium), Line Height 10px (leading-[10px])
- **Icon Size**: 12px (w-3 h-3)
- **Border Radius**: 6px (rounded-md)

**Medium:**
- **Height**: 28px
- **Padding**: 8px 12px (px-3 py-2)
- **Font**: Urbanist, 12px, Weight 600 (Semibold), Line Height 12px (leading-3)
- **Icon Size**: 14px (w-3.5 h-3.5)
- **Border Radius**: 8px (rounded-lg)

**Large:**
- **Height**: 36px
- **Padding**: 10px 14px (px-3.5 py-2.5)
- **Font**: Urbanist, 14px, Weight 500 (Medium), Line Height 16px (leading-4)
- **Icon Size**: 16px (w-4 h-4)
- **Border Radius**: 8px (rounded-lg)

---

#### Button Types

**Primary Button (Filled):**
- **Background**: #164E3F (Teal-900)
- **Color**: #FAFAFA (Neutral-50)
- **Icon Color**: #FAFAFA (Neutral-50)
- **States**:
  - Hover: Background #0F3D30 (Darker)
  - Active: Background #0A2B21 (Even Darker)
  - Disabled: Opacity 0.5

**Secondary Button (Light Fill):**
- **Background**: #F5F5F4 (Stone-100)
- **Color**: #164E3F (Teal-900)
- **Icon Color**: #164E3F (Teal-900)
- **States**:
  - Hover: Background #E7E5E4 (Stone-200)
  - Active: Background #D6D3D1 (Stone-300)

**Outline Button:**
- **Background**: Transparent
- **Border**: 1px solid #E5E5E5 (Neutral-200)
- **Color**: #164E3F (Teal-900)
- **Icon Color**: #164E3F (Teal-900)
- **States**:
  - Hover: Background #F7F8F8, Border #DBDDDF

**Ghost Button (Text Only):**
- **Background**: Transparent
- **Color**: #164E3F (Teal-900)
- **Icon Color**: #164E3F (Teal-900)
- **Padding**: 2px (px-0.5)
- **States**:
  - Hover: Background rgba(22, 78, 63, 0.05)

---

#### Button Variants with Icons

**Text Only:**
- Padding: Standard for size
- No icon spacing

**Icon Left:**
- **Gap**: 4px (gap-1) for Small, 4px (gap-1) for Medium, 4px (gap-1) for Large
- **Icon**: Before text
- **Padding**: Adjust left padding +2px

**Icon Right:**
- **Gap**: 2px (gap-0.5) for Small/Medium, 2px (gap-0.5) for Large
- **Icon**: After text
- **Padding**: Adjust right padding +2px

**Icon Both Sides:**
- **Gap Left**: 4px (gap-1)
- **Gap Right**: 2px (gap-0.5)
- **Padding**: Adjust both sides

**Icon Only:**
- **Padding**: 6px (p-1.5) for Small, 8px (p-2) for Medium, 10px (p-2.5) for Large
- **Size**: Square (24px, 28px, 36px respectively)
- **Border Radius**: Same as button size

---

#### Pill Buttons (Navigation)

**Large Pill:**
- **Height**: 40px (h-10)
- **Padding**: 8px 16px 8px 12px (pl-4 pr-3 py-2) with icon, 8px 16px without
- **Border Radius**: 24px (rounded-3xl)
- **Font**: Urbanist, 14px, Weight 600 (Semibold), Line Height 16px (leading-4)
- **Icon Size**: 24px (w-6 h-6)
- **Gap**: 12px (gap-3)

**States:**
- **Active**: Background #ECFCCB (Lime-200), Color #262626 (Zinc-800), Icon #262626
- **Inactive**: Background Transparent, Color #737373 (Neutral-500), Icon #737373
- **Hover (inactive)**: Background rgba(0, 0, 0, 0.05)

**Icon Only Pill:**
- **Size**: 40px × 40px (p-2)
- **Border Radius**: 24px (rounded-3xl)
- **Icon Size**: 24px (w-6 h-6)

**With Divider:**
- **Divider**: 1px wide (w-0), Height 20px (h-5), Color #D6D3D1 (Stone-300) or #262626 (Zinc-800 when active)
- **Spacing**: 12px gap before divider, 8px padding after

---

#### Icon Buttons

**Small Icon Button:**
- **Size**: 22px × 22px (p-1.5)
- **Icon**: 12px (w-3 h-3)
- **Border Radius**: 6px (rounded-md) or 5px (rounded-[5px]) for ghost

**Medium Icon Button:**
- **Size**: 28px × 28px (p-2)
- **Icon**: 16px (w-4 h-4)
- **Border Radius**: 8px (rounded-lg)

**Large Icon Button:**
- **Size**: 36px × 36px (p-2.5)
- **Icon**: 20px (w-5 h-5)
- **Border Radius**: 8px (rounded-lg) or 20px (rounded-[20px]) for pill style

**With Badge:**
- **Badge Position**: Top-right, offset 2-6px depending on button size
- **Badge**: See Notification Badges section

---

#### Button Groups

**Attached Buttons (No Gap):**
- **Gap**: 0.5px (gap-px)
- **Border Radius**:
  - First button: rounded-tl-md rounded-bl-md
  - Middle buttons: No radius
  - Last button: rounded-tr-md rounded-br-md
- **Background wrapper**: #F7F8F8 (Neutral-50) or #F5F5F4 (Stone-100)
- **Border Radius wrapper**: 8px (rounded-lg)

**Separated Tabs:**
- **Gap**: 2px (gap-0.5)
- **Background wrapper**: #F5F5F4 (Stone-100)
- **Border Radius wrapper**: 8px (rounded-lg)
- **Active button**: Primary style
- **Inactive buttons**: Secondary style
- **Equal width**: Use flex-1 on all buttons

---

#### Vertical Icon Button

**Layout:**
- **Direction**: Column (flex-col)
- **Padding**: 4px vertical (py-1)
- **Gap**: 6px (gap-1.5)
- **Min Width**: 44px (min-w-11)
- **Alignment**: Center

**Icon:**
- **Size**: 24px (w-6 h-6)
- **Color**: #164E3F (Teal-900)

**Label:**
- **Font**: Urbanist, 10px, Weight 600 (Semibold), Line Height 10px
- **Color**: #164E3F (Teal-900)
- **Max width**: Wrap text if needed

**States:**
- **Hover**: Background rgba(22, 78, 63, 0.05), Border-radius 8px
- **Active**: Background #E8F5FF (Blue-Subtle)

---

### 3. Inputs

#### Text Input

- **Height**:
  - Small: 32px
  - Medium: 40px
  - Large: 48px
- **Padding**: 12px 16px
- **Radius**: 8px (0.5rem / rounded-base)
- **Border**: 1px solid #DBDDDF (Gray-Line)
- **States**:
  - Focus: Border #43ABFF (Blue-10), Shadow 0 0 0 3px rgba(67, 171, 255, 0.1)
  - Error: Border #FF434E (Red), Background #FFF4F4 (Red-Subtle-2)
  - Disabled: Background #F2F3F4 (Gray-BG), Color #B3B7BA (Gray-10), Opacity 0.6

#### Textarea

- **Min Height**: 96px
- **Padding**: 12px 16px
- **Radius**: 8px (0.5rem)
- **Resize**: Vertical only

#### Select

- **Height**: 40px (Medium)
- **Padding**: 12px 16px, Padding-right: 40px
- **Icon**: Chevron Down (16px), Position: Right 12px

---

### 4. Badges & Tags

#### Notification Badges (Числовые индикаторы)

**Большой размер:**
- **Size**: 20px × 20px (w-5 h-5)
- **Padding**: 2px (p-0.5)
- **Border Radius**: 10px (rounded-[10px])
- **Background**: #FF434E (Red)
- **Color**: #FAFAFA (Neutral-50)
- **Font**: Urbanist, 12px, Weight 400, Line Height 12px (leading-3)
- **Content**: Числа (например, "99")

**Большой размер (точка):**
- **Size**: 10px × 10px (w-2.5 h-2.5)
- **Background**: #FF434E (Red)
- **Border Radius**: 10px (rounded-[10px])
- **No text**: Только индикатор

**Маленький размер:**
- **Size**: 14px × 14px (w-3.5 h-3.5)
- **Padding**: 2px (p-0.5)
- **Border Radius**: 10px (rounded-[10px])
- **Background**: #FF434E (Red)
- **Color**: #FAFAFA (Neutral-50)
- **Font**: Urbanist, 8px, Weight 400, Line Height 10.4px
- **Content**: Числа (например, "99")

**Маленький размер (точка):**
- **Size**: 8px × 8px (w-2 h-2)
- **Background**: #FF434E (Red)
- **Border Radius**: 10px (rounded-[10px])
- **No text**: Только индикатор

---

#### Status Badges

**Outlined (Обводка)**
- **Padding**: 6px 4px (px-1.5 py-0.5)
- **Border Radius**: 4px (rounded)
- **Border**: 1px solid #E5E5E5 (Neutral-200)
- **Font**: Urbanist, 10px, Weight 400, Line Height 12px (leading-3)
- **Варианты**:
  - Completed: Color #164E3F (Teal-900)
  - Pending: Color #EAB308 (Yellow-500)
  - Failed: Color #FF434E (Red-500)

**Filled Small (Заливка, маленький)**
- **Padding**: 6px 4px (px-1.5 py-0.5)
- **Border Radius**: 4px (rounded)
- **Font**: Urbanist, 10px, Line Height 12px (leading-3)
- **Варианты**:
  - Completed: Background #164E3F (Teal-900), Color #ECFCCB (Lime-200), Weight 600 (Semibold)
  - Pending: Background #ECFCCB (Lime-200), Color #164E3F (Teal-900), Weight 400
  - Failed: Background #FECACA (Rose-200), Color #FF434E (Red-500), Weight 400

**Filled Medium (Заливка, средний)**
- **Padding**: 8px 4px (px-2 py-1)
- **Border Radius**: 6px (rounded-md)
- **Font**: Urbanist, 12px, Line Height 16px (leading-4)
- **Варианты**:
  - Completed: Background #164E3F (Teal-900), Color #ECFCCB (Lime-200), Weight 500 (Medium)
  - Pending: Background #ECFCCB (Lime-200), Color #164E3F (Teal-900), Weight 400
  - Failed: Background #FECACA (Rose-200), Color #FF434E (Red-500), Weight 400

**Pill Badges (Таблетка)**
- **Padding**: 10px 4px (px-2.5 py-1)
- **Border Radius**: 16px (rounded-2xl)
- **Font**: Urbanist, 12px, Line Height 16px (leading-4)
- **Варианты**:
  - Paid: Background #164E3F (Teal-900), Color #ECFCCB (Lime-200), Weight 500 (Medium)
  - Pending: Background #ECFCCB (Lime-200), Color #164E3F (Teal-900), Weight 400
  - Overdue: Background #FECACA (Rose-200), Color #FF434E (Red-500), Weight 400
  - Unpaid: Background #D6D3D1 (Stone-300), Color #262626 (Zinc-800), Weight 400

---

#### Tag

- **Padding**: 6px 12px
- **Radius**: 8px (0.5rem / rounded-base)
- **Font Size**: 14px (0.875rem)
- **Close Button**: Size 16px, Color #757D83, Hover #333E47

---

#### Hashtag Tag

**Hashtag Tag Container:**
- **Padding Left**: 10px (pl-2.5)
- **Padding Right**: 12px (pr-3)
- **Padding Vertical**: 8px (py-2)
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: 8px (rounded-lg)
- **Display**: Inline-flex
- **Alignment**: justify-center items-center
- **Gap**: 0 (no gap, elements are adjacent)

**Hash Symbol (#):**
- **Font**: Urbanist, 12px (text-xs), Weight 500 (Medium), Line Height 16px (leading-4)
- **Color**: #D6D3D1 (Stone-300)
- **Content**: "#"
- **Alignment**: justify-start

**Tag Text:**
- **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Alignment**: justify-start
- **Example**: "FinancialPlanning", "Marketing", "Design"

**Spacing:**
- Horizontal padding asymmetric: 10px left, 12px right
- Vertical padding: 8px top/bottom
- No gap between hash and text (adjacent)

**Use Cases:**
- Social media hashtags
- Content categorization
- Topic tagging
- Filtering by category
- Search keywords

**States:**

**Default:**
- Background: Stone-100 (#F5F5F4)
- Hash: Stone-300 (#D6D3D1)
- Text: Zinc-800 (#27272A)

**Hover:**
- Background: Stone-200 (#E7E5E4)
- Cursor: pointer
- Scale: 1.02
- Transition: 150ms ease

**Active/Selected:**
- Background: Teal-900 (#164E3F)
- Hash: Lime-200 (#ECFCCB)
- Text: Lime-200 (#ECFCCB)

**Disabled:**
- Background: Stone-50 (#FAFAF9)
- Hash: Stone-200 (#E7E5E4)
- Text: Stone-400 (#A8A29E)
- Cursor: not-allowed
- Opacity: 0.6

**Variants:**

**Removable Hashtag:**
- Add close button (×) on the right
- Close icon: 12px, Stone-400, hover Stone-600
- Extra padding right: 8px for close button

**Colored Hashtags:**
- **Blue**: Background Blue-50 (#EFF6FF), Hash Blue-300 (#93C5FD), Text Blue-700 (#1D4ED8)
- **Green**: Background Emerald-50 (#ECFDF5), Hash Emerald-300 (#6EE7B7), Text Emerald-700 (#047857)
- **Purple**: Background Purple-50 (#FAF5FF), Hash Purple-300 (#D8B4FE), Text Purple-700 (#7E22CE)
- **Orange**: Background Orange-50 (#FFF7ED), Hash Orange-300 (#FDBA74), Text Orange-700 (#C2410C)

**Size Variants:**

**Small (Compact):**
- Padding: 6px 8px (pl-2 pr-2 py-1.5)
- Font: 10px (text-[10px])
- Border Radius: 6px (rounded-md)

**Medium (Default):**
- Padding: 10px 12px (pl-2.5 pr-3 py-2)
- Font: 12px (text-xs)
- Border Radius: 8px (rounded-lg)

**Large:**
- Padding: 12px 16px (pl-3 pr-4 py-3)
- Font: 14px (text-sm)
- Border Radius: 10px (rounded-[10px])

**Best Practices:**
- Keep hashtag text concise (max 20 characters)
- Use CamelCase for multi-word tags (#FinancialPlanning)
- Avoid spaces in hashtag text
- Provide visual feedback on hover/click
- Support keyboard navigation (Tab, Enter, Backspace)
- Allow filtering/grouping by hashtags
- Make removable in edit mode

**Accessibility:**
- ARIA label: "Hashtag: [tag name]"
- Keyboard accessible: focusable and activatable
- Screen reader: announce as "tag" or "hashtag"
- Focus indicator: 2px outline Teal-900
- Sufficient color contrast (4.5:1 minimum)

**Layout Patterns:**

**Horizontal List:**
```
#Design  #UI  #UX  #Frontend
```
- Gap: 8px (gap-2)
- Flex wrap enabled
- Alignment: items-center

**Vertical Stack:**
```
#Design
#UI
#UX
```
- Gap: 6px (gap-1.5)
- Full width tags

**Grid Layout:**
```
#Design    #UI       #UX
#Frontend  #Backend  #Mobile
```
- Grid: auto-fit columns
- Gap: 8px (gap-2)
- Responsive columns

---

### 5. Forms

#### Search Inputs

**Large Search Input:**
- **Width**: 240px (w-60)
- **Padding**: 10px 16px 10px 12px (px-4 py-2.5)
- **Background**: #F4F4F5 (Zinc-100)
- **Border**: 1px solid #F4F4F5 (Zinc-100)
- **Border Radius**: 20px (rounded-[20px])
- **Font**: Urbanist, 12px, Weight 400, Line Height 16px (leading-4)
- **Placeholder Color**: #737373 (Neutral-500)
- **Icon**: 16px (w-4 h-4), Color #164E3F (Teal-900)
- **Gap**: 6px (gap-1.5)

**Medium Search Input:**
- **Width**: 240px (w-60)
- **Padding**: 6px 12px 6px 14px (pl-3.5 pr-3 py-1.5)
- **Background**: #F4F4F5 (Zinc-100)
- **Border**: 1px solid #F4F4F5 (Zinc-100)
- **Border Radius**: 16px (rounded-2xl)
- **Font**: Urbanist, 12px, Weight 400, Line Height 16px (leading-4)
- **Icon**: 16px (w-4 h-4)
- **Gap**: 6px (gap-1.5)

**Small Search Input:**
- **Width**: 224px (w-56)
- **Padding**: 6px 10px 6px 12px (pl-3 pr-2.5 py-1.5)
- **Background**: #F4F4F5 (Zinc-100)
- **Border**: 1px solid #F4F4F5 (Zinc-100)
- **Border Radius**: 16px (rounded-2xl)
- **Font**: Urbanist, 12px, Weight 400, Line Height 12px (leading-3)
- **Icon**: 14px (w-3.5 h-3.5)
- **Gap**: 4px (gap-1)

---

#### Input Fields

**Large Input with Label:**
- **Width**: 240px (w-60)
- **Label**:
  - Padding Bottom: 12px (pb-3)
  - Font: Urbanist, 14px, Weight 600 (Semibold), Line Height 16px (leading-4)
  - Color: #262626 (Zinc-800)
- **Input**:
  - Padding: 12px 14px (px-3.5 py-3)
  - Background: #FAFAFA (Neutral-50)
  - Border: 1px solid #E5E5E5 (Neutral-200)
  - Border Radius: 8px (rounded-lg)
  - Font: Urbanist, 14px, Weight 400, Line Height 16px (leading-4)
  - Placeholder Color: #262626 (Zinc-800)
- **Icons**: 16px (w-4 h-4), Color #164E3F (Teal-900)
- **Gap**: 6px (gap-1.5)

**Medium Input:**
- **Width**: 240px (w-60)
- **Padding**: 8px 12px (px-3 py-2)
- **Background**: #F5F5F5 (Neutral-100)
- **Border**: 1px solid #F5F5F5 (Neutral-100)
- **Border Radius**: 10px (rounded-[10px])
- **Font**: Lato, 12px, Weight 400, Line Height 16px (leading-4)
- **Placeholder Color**: #52525B (Zinc-600)
- **Icons**: 16px (w-4 h-4), Color #171717 (Neutral-900)
- **Gap**: 6px (gap-1.5)

**Small Input with Label:**
- **Width**: 176px (w-44)
- **Padding**: 6px 12px (px-3 py-1.5)
- **Background**: #F5F5F5 (Neutral-100)
- **Border Radius**: 10px (rounded-[10px])
- **Label**:
  - Font: Lato, 10px, Weight 400, Line Height 12px (leading-3)
  - Color: #171717 (Neutral-900)
  - Margin Bottom: 2px (gap-0.5)
- **Input**:
  - Font: Lato, 12px, Weight 400, Line Height 20px (leading-5)
  - Placeholder Color: #52525B (Zinc-600)
- **Icons**: 16px (w-4 h-4)
- **Gap**: 6px (gap-1.5)

**Compact Input:**
- **Width**: 224px (w-56)
- **Padding**: 6px 8px (px-2 py-1.5)
- **Background**: #F5F5F5 (Neutral-100)
- **Border**: 1px solid #F5F5F5 (Neutral-100)
- **Border Radius**: 8px (rounded-lg)
- **Font**: Lato, 12px, Weight 400, Line Height 20px (leading-5)
- **Icons**: 14px (w-3.5 h-3.5), Color #171717 (Neutral-900)
- **Gap**: 4px (gap-1)

---

#### Checkboxes

**Small Checkbox:**
- **Size**: 12px × 12px (w-3 h-3)
- **Background**: #F5F5F5 (Neutral-100)
- **Border**: 1px solid #E7E5E4 (Stone-200)
- **Border Radius**: 3px (rounded-[3px])
- **States**:
  - Unchecked: Background #F5F5F5, Border #E7E5E4
  - Checked: Background #D1FAE5 (Emerald-100), Border #D1FAE5, Checkmark 6px (w-1.5 h-1) with 1.5px stroke, Color #171717
  - Indeterminate: Background #D1FAE5, Border #D1FAE5, Line 6px width with 1.5px stroke, Color #171717
  - Hover: Border color darkens
  - Disabled: Opacity 0.5

**Medium Checkbox:**
- **Size**: 16px × 16px (w-4 h-4)
- **Background**: #F5F5F5 (Neutral-100)
- **Border**: 1px solid #E7E5E4 (Stone-200)
- **Border Radius**: 4px (rounded)
- **States**:
  - Unchecked: Background #F5F5F5, Border #E7E5E4
  - Checked: Background #D1FAE5 (Emerald-100), Border #D1FAE5, Checkmark 8px (w-2 h-1.5) with 2px stroke, Color #171717

**Large Checkbox:**
- **Size**: 20px × 20px (w-5 h-5)
- **Background**: #F5F5F5 (Neutral-100)
- **Border**: 1.5px solid #E7E5E4 (Stone-200)
- **Border Radius**: 6px (rounded-md)
- **States**:
  - Unchecked: Background #F5F5F5, Border #E7E5E4
  - Checked: Background #D1FAE5 (Emerald-100), Border #D1FAE5, Checkmark 10px (w-2.5 h-2) with 2.75px stroke, Color #171717

---

#### Toggle Switches

**Toggle Switch:**
- **Height**: 16px total (with 2px padding)
- **Border Radius**: 8px (rounded-lg)
- **Circle**: 12px × 12px (w-3 h-3), Background #FFFFFF (White), Border Radius full (rounded-full)

**States:**
- **Off (Inactive)**:
  - Padding: 2px 14px 2px 2px (pl-0.5 pr-3.5 py-0.5)
  - Background: #E7E5E4 (Stone-200)
  - Circle position: Left
  - Width: ~30px total

- **On (Active)**:
  - Padding: 2px 2px 2px 14px (pl-3.5 pr-0.5 py-0.5)
  - Background: #D1FAE5 (Emerald-100)
  - Circle position: Right
  - Width: ~30px total

**Animation**: Smooth transition 200ms ease-in-out for background and circle position

---

#### Form Layout

- **Label**:
  - Margin Bottom: 8px (0.5rem) to 12px
  - Font Weight: 500-600 (Medium to Semibold)
  - Font Size: 10px-14px depending on input size
- **Field Group**:
  - Margin Bottom: 24px (1.5rem)
- **Helper Text**:
  - Margin Top: 6px (0.375rem)
  - Font Size: 12px (0.75rem)
  - Color: #737373 (Neutral-500)
- **Error Message**:
  - Color: #FF434E (Red)
  - Font Size: 12px (0.75rem)

**Input States:**
- **Focus**: Border color #164E3F (Teal-900) or #43ABFF (Blue-10), Shadow 0 0 0 3px rgba(67, 171, 255, 0.1)
- **Error**: Border #FF434E (Red), Background #FFF4F4 (Red-Subtle-2)
- **Disabled**: Background #F2F3F4 (Gray-BG), Color #B3B7BA (Gray-10), Opacity 0.6
- **Hover**: Border color slightly darkens

---

### 6. Tables

Компонент для отображения табличных данных с сортировкой, фильтрацией и адаптивностью.

---

#### Table Container

**Table Wrapper:**
- **Width**: 612px (w-[612px]) - example width, can be self-stretch
- **Padding**: 20px (p-5)
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Display**: Inline-flex, flex-col
- **Gap**: 20px (gap-5) between rows
- **Overflow**: Hidden

---

#### Table Header Row

**Header Container:**
- **Full Width**: self-stretch
- **Padding**: 10px (p-2.5)
- **Border Top**: 1px solid #E5E5E5 (Neutral-200)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-between
- **Layout**: Horizontal row

---

##### Table Header Cell

**Header Cell (with Sorting):**
- **Display**: Flex
- **Alignment**: items-end, justify-start
- **Gap**: 0 (icon adjacent to text)

**Column Widths:**
- **Transaction Name**: 144px (w-36)
- **Date & Time**: 64px (w-16)
- **Amount**: 48px (w-12) or 64px (w-16)
- **Note**: 128px (w-32)
- **Status**: 64px (w-16)

**Header Text:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal), Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Example**: "Transaction Name", "Date & Time", "Amount"

**Sort Icon Container:**
- **Size**: 12px × 12px (w-3 h-3)
- **Position**: Relative
- **Display**: Adjacent to text (items-end alignment)

**Sort Icon Arrows:**
- **Size**: 4px × 2.62px (w-1 h-[2.62px]) each arrow
- **Position**: Absolute
- **Up Arrow**: left 3.75px, top 2.62px
- **Down Arrow**: left 3.75px, top 6.75px
- **Background**: #737373 (Neutral-500)
- **Use case**: Indicates sortable column
- **States**:
  - Both visible: Unsorted
  - One highlighted: Sorted (ascending/descending)

---

#### Table Data Row (Full Width)

**Row Container:**
- **Full Width**: self-stretch
- **Padding**: 10px (p-2.5)
- **Border Top**: 1px solid #E5E5E5 (Neutral-200)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-between

---

##### Table Cells (Full Width Layout)

**Transaction Name Cell:**
- **Width**: 144px (w-36)
- **Display**: Inline-flex, flex-col
- **Gap**: 2px (gap-0.5)

**Primary Text (Transaction Name):**
- **Font**: Urbanist, 10px (text-[10px]), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #27272A (Zinc-800)
- **Example**: "Dinner at Italian Restaurant"

**Secondary Text (Category):**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal), Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Example**: "Dining Out", "Shopping", "Transport"

---

**Date & Time Cell:**
- **Width**: 64px (w-16)
- **Display**: Inline-flex, flex-col
- **Gap**: 2px (gap-0.5)

**Date:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #27272A (Zinc-800)
- **Format**: "2024-03-01" (YYYY-MM-DD)

**Time:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal), Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Format**: "04:28:48" (HH:MM:SS)

---

**Amount Cell:**
- **Width**: 48px (w-12)
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-center

**Amount Text:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Format**: "$226.25", "€150.00"

---

**Note Cell:**
- **Width**: 128px (w-32)
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-center

**Note Text:**
- **Full Width**: self-stretch
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal), Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Line Clamp**: 2 lines (line-clamp-2)
- **Example**: "Dining out with family at a local Italian restaurant."

---

**Status Cell:**
- **Width**: 64px (w-16)
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-center

**Status Badge:**
- **Padding Horizontal**: 6px (px-1.5)
- **Padding Vertical**: 2px (py-0.5)
- **Border Radius**: Default (rounded)
- **Outline**: 1px solid #E5E5E5 (Neutral-200)
- **Outline Offset**: -1px (outline-offset-[-1px]) - внутренняя обводка
- **Display**: Inline-flex
- **Gap**: 10px (gap-2.5)

**Status Text:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal), Line Height 12px (leading-3)
- **Color**: #164E3F (Teal-900) - для Completed
- **States**:
  - Completed: Teal-900
  - Pending: Yellow-600
  - Failed: Red-500
  - Cancelled: Stone-500

---

#### Table Variants & Additional Cells

##### Account Cell (with Payment Card Icon)

**Account Cell:**
- **Width**: 160px (w-40)
- **Display**: Flex
- **Alignment**: items-center, justify-start
- **Gap**: 6px (gap-1.5)

**Card Icon Container:**
- **Width**: 24px (w-6)
- **Height**: 16px (h-4)
- **Position**: Relative
- **Border Radius**: 3px (rounded-[3px])
- **Outline**: 1px solid #E5E5E5 (Neutral-200)
- **Outline Offset**: -1px (outline-offset-[-1px])

**Mastercard Logo Elements:**
- **Left Circle**:
  - Size: 10px × 10px (w-2.5 h-2.5)
  - Position: Absolute, left 4px, top 3px
  - Background: #6B7280 (Gray-600)
  - Border Radius: Full (rounded-full)
- **Right Circle**:
  - Size: 10px × 10px (w-2.5 h-2.5)
  - Position: Absolute, left 10px, top 3px
  - Background: #ECFCCB (Lime-200)
  - Opacity: 0.8
  - Border Radius: Full (rounded-full)
- **Overlap Bar**:
  - Size: 4px × 8px (w-1 h-2)
  - Position: Absolute, left 10px, top 4px
  - Background: #164E3F (Teal-900)
  - Opacity: 0.8

**Account Name Text:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal), Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Line Clamp**: 2 lines (line-clamp-2)
- **Example**: "Freedom Unlimited Mastercard", "Visa Platinum Card"

**Other Card Types:**
- **Visa**: Blue circle + Yellow overlap
- **Amex**: Blue square
- **Discover**: Orange circle
- **Generic**: Gray icon

---

##### Alternative Header Styles

**Light Header (Alternative):**
- **Padding Horizontal**: 6px (px-1.5)
- **Padding Vertical**: 12px (py-3)
- **Border**: None or subtle border-bottom
- **Background**: Transparent

**Header Text (Light):**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal), Line Height 12px (leading-3)
- **Color**: #D6D3D1 (Stone-300) - lighter than default
- **Use case**: Minimal table design, less visual weight

**Sort Icons (Light):**
- **Color**: #D6D3D1 (Stone-300)
- States same as default

---

##### Status Badge - Filled Variant

**Filled Status Badge:**
- **Padding Horizontal**: 6px (px-1.5)
- **Padding Vertical**: 2px (py-0.5)
- **Border Radius**: Default (rounded)
- **Display**: Inline-flex
- **Gap**: 10px (gap-2.5)
- **No Outline**: Solid fill instead

**Completed (Filled):**
- **Background**: #164E3F (Teal-900)
- **Text**: #ECFCCB (Lime-200)
- **Font Weight**: 600 (Semibold)

**Pending (Filled):**
- **Background**: #FEF08A (Yellow-200)
- **Text**: #854D0E (Yellow-900)
- **Font Weight**: 600 (Semibold)

**Failed (Filled):**
- **Background**: #FECACA (Red-200)
- **Text**: #EF4444 (Red-500)
- **Font Weight**: 600 (Semibold)

**Processing (Filled):**
- **Background**: #BFDBFE (Blue-200)
- **Text**: #1D4ED8 (Blue-700)
- **Font Weight**: 600 (Semibold)

**Cancelled (Filled):**
- **Background**: #E7E5E4 (Stone-200)
- **Text**: #57534E (Stone-600)
- **Font Weight**: 400 (Normal)

---

##### Amount Cell - Color Coded

**Amount with Color Coding:**
- Same layout as standard amount cell
- **Color** depends on transaction type

**Expense/Debit (Negative):**
- **Font**: Urbanist, 10px (text-[10px]), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #EF4444 (Red-500)
- **Prefix**: "-" or no prefix
- **Example**: "$120.75", "-$50.00"

**Income/Credit (Positive):**
- **Font**: Urbanist, 10px (text-[10px]), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #10B981 (Emerald-500)
- **Prefix**: "+" optional
- **Example**: "+$500.00", "$1,200.50"

**Neutral (Zero or Pending):**
- **Font**: Urbanist, 10px (text-[10px]), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Example**: "$0.00", "Pending"

**Large Amounts:**
- **Color**: Darker shade for emphasis
- **Expense**: #DC2626 (Red-600)
- **Income**: #059669 (Emerald-600)

---

##### Extended Table Example (Full Width with Account)

**Column Layout:**
1. Transaction Name: 96px (w-24)
2. Account: 160px (w-40)
3. Date & Time: 64px (w-16)
4. Amount: 48px (w-12)
5. Status: 64px (w-16)

**Header Row:**
- **Padding**: 6px/12px (px-1.5 py-3)
- **Text Color**: Stone-300 (#D6D3D1) - light variant
- **Border**: None (cleaner look)

**Data Row:**
- **Padding**: 6px/12px (px-1.5 py-3)
- **Border Top**: 1px Neutral-200
- **Transaction**: "Online Subscription" + "Health & Fitness"
- **Account**: [Mastercard Icon] + "Freedom Unlimited Mastercard"
- **Date/Time**: "2024-09-24" + "14:30"
- **Amount**: "$120.75" (Red-500 for expense)
- **Status**: Filled badge - Teal-900 background, Lime-200 text

---

##### Table with Row Selection (Checkboxes)

**Wide Table Container:**
- **Width**: 1139px (w-[1139px]) - full desktop width
- **Layout**: Checkbox + Flex content

---

**Header Row with Checkbox:**

**Row Container:**
- **Width**: 1139px (w-[1139px])
- **Padding Horizontal**: 10px (px-2.5)
- **Padding Vertical**: 12px (py-3)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 20px (gap-5)

**Select All Checkbox:**
- **Size**: 12px × 12px (w-3 h-3)
- **Position**: Relative
- **Background**: #F5F5F5 (Neutral-100)
- **Border Radius**: 3px (rounded-[3px])
- **Outline**: 1px solid #E7E5E4 (Stone-200)
- **Use case**: Select/deselect all rows

**Header Content:**
- **Flex**: 1 (flex-1)
- **Display**: Flex
- **Alignment**: items-center, justify-between
- **Contains**: All column headers

**Column Widths (with selection):**
1. **Transaction Name**: 160px (w-40)
2. **Account**: 192px (w-48)
3. **Transaction ID**: 80px (w-20)
4. **Date & Time**: 64px (w-16)
5. **Amount**: 48px (w-12)
6. **Note**: 192px (w-48)
7. **Status**: 80px (w-20)

---

**Data Row with Checkbox:**

**Row Container:**
- **Width**: 1139px (w-[1139px])
- **Padding Horizontal**: 10px (px-2.5)
- **Padding Vertical**: 16px (py-4)
- **Border Top**: 1px solid #E5E5E5 (Neutral-200)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 20px (gap-5)

**Row Checkbox:**
- **Size**: 12px × 12px (w-3 h-3)
- **Position**: Relative
- **Background**: #F5F5F5 (Neutral-100)
- **Border Radius**: 3px (rounded-[3px])
- **Outline**: 1px solid #E7E5E4 (Stone-200)

**Checkbox States:**
- **Unchecked**: Neutral-100 background, Stone-200 outline
- **Checked**: Teal-900 background, checkmark icon (Lime-200)
- **Indeterminate** (some selected): Teal-900 background, minus icon
- **Hover**: Stone-300 outline, slight scale 1.1
- **Disabled**: Stone-100 background, Stone-200 outline, opacity 0.5

---

##### Transaction Name Cell with Icon

**Cell Container:**
- **Width**: 160px (w-40)
- **Display**: Flex
- **Alignment**: items-center, justify-start
- **Gap**: 10px (gap-2.5)

**Category Icon Container:**
- **Size**: 28px × 28px (w-7 h-7)
- **Background**: #ECFCCB (Lime-200)
- **Border Radius**: 56px (rounded-[56px]) - fully circular
- **Position**: Relative
- **Overflow**: Hidden

**Icon:**
- **Size**: 16px × 16px (w-4 h-4)
- **Position**: Absolute, left 7px, top 7px (centered)
- **Overflow**: Hidden

**Icon Graphic:**
- **Size**: 12px × 12px (w-3 h-3)
- **Position**: Absolute, left 1.5px, top 1.5px
- **Background**: #27272A (Zinc-800)

**Text Container:**
- **Display**: Inline-flex, flex-col
- **Gap**: 2px (gap-0.5)

**Primary Text (Transaction Name):**
- **Font**: Urbanist, 12px (text-xs), Weight 500 (Medium), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Example**: "Comcast Bill Payment", "Netflix Subscription"

**Secondary Text (Category):**
- **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal), Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Example**: "Food & Dining", "Entertainment", "Utilities"

**Icon Background Colors by Category:**
- **Food & Dining**: Lime-200 (#ECFCCB)
- **Entertainment**: Purple-200 (#E9D5FF)
- **Utilities**: Blue-200 (#BFDBFE)
- **Shopping**: Rose-200 (#FECACA)
- **Transport**: Orange-200 (#FED7AA)
- **Health**: Emerald-200 (#A7F3D0)
- **Default**: Stone-200 (#E7E5E4)

---

##### Enhanced Data Cells (12px Font)

**Account Cell (Enhanced):**
- **Width**: 192px (w-48)
- **Gap**: 6px (gap-1.5)
- **Font**: Urbanist, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
- **Card Icon**: Same as before (24×16px)

**Transaction ID Cell:**
- **Width**: 80px (w-20)
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-center

**ID Text:**
- **Font**: Urbanist, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Format**: "4567890123", "TX-12345"

**Date & Time Cell (Enhanced):**
- **Width**: 64px (w-16)
- **Font**: Urbanist, 12px (text-xs), Weight 400, Line Height 16px/12px
- **Date**: leading-4 (16px)
- **Time**: leading-3 (12px), Neutral-500

**Amount Cell (Enhanced):**
- **Width**: 48px (w-12)
- **Border Radius**: 8px (rounded-lg)
- **Gap**: 4px (gap-1)

**Amount Text:**
- **Font**: Urbanist, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
- **Color**: Red-500 for expenses, Emerald-500 for income
- **Format**: "-$350.00", "+$500.00"

**Note Cell (Enhanced):**
- **Width**: 192px (w-48)
- **Gap**: 6px (gap-1.5)

**Note Text:**
- **Font**: Urbanist, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Line Clamp**: 2 lines (line-clamp-2)
- **Example**: "Monthly entertainment subscription"

**Status Cell (Enhanced):**
- **Width**: 80px (w-20)
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-center

**Status Badge (Enhanced):**
- **Padding Horizontal**: 8px (px-2)
- **Padding Vertical**: 4px (py-1)
- **Background**: #164E3F (Teal-900)
- **Border Radius**: 6px (rounded-md)
- **Display**: Inline-flex
- **Gap**: 10px (gap-2.5)

**Status Text:**
- **Font**: Urbanist, 12px (text-xs), Weight 500 (Medium), Line Height 16px (leading-4)
- **Color**: #ECFCCB (Lime-200)

---

##### Table Selection Features

**Bulk Actions Toolbar:**
- Appears when rows are selected
- **Content**: "[N] selected" + Action buttons (Delete, Export, Archive)
- **Position**: Top of table or floating
- **Background**: Blue-50
- **Padding**: 12px
- **Border**: 1px Blue-200

**Selection States:**
- **No selection**: Toolbar hidden, checkboxes default
- **Some selected**: Toolbar visible, header checkbox indeterminate
- **All selected**: Toolbar visible, header checkbox checked

**Keyboard Shortcuts:**
- **Shift+Click**: Select range
- **Cmd/Ctrl+A**: Select all visible rows
- **Escape**: Deselect all

**Visual Feedback:**
- **Selected row**: Background Blue-50 (#EFF6FF)
- **Selected row hover**: Background Blue-100 (#DBEAFE)
- **Checkbox animation**: Smooth check/uncheck (200ms ease)

---

#### Table Data Row (Compact Width)

**Compact Row Container:**
- **Width**: 320px (w-80)
- **Padding Horizontal**: 4px (px-1)
- **Padding Vertical**: 10px (py-2.5)
- **Border Top**: 1px solid #E5E5E5 (Neutral-200)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-between

**Column Widths (Compact):**
- **Transaction Name**: 128px (w-32)
- **Date & Time**: 64px (w-16)
- **Amount + Status**: 64px (w-16)

---

##### Compact Layout Cells

**Transaction Name Cell (Compact):**
- **Width**: 128px (w-32)
- **Font**: Urbanist, 12px (text-xs), Weight 600/400, Line Height 12px (leading-3)
- **Same structure**: Primary + Secondary text

**Date & Time Cell (Compact):**
- **Width**: 64px (w-16)
- **Font**: Urbanist, 12px (text-xs), Weight 600/400, Line Height 12px (leading-3)
- **Same structure**: Date + Time

**Amount & Status Cell (Compact):**
- **Width**: 64px (w-16)
- **Display**: Inline-flex, flex-col
- **Gap**: 4px (gap-1)
- **Alignment**: items-start, justify-center

**Amount (Top):**
- **Font**: Urbanist, 12px (text-xs), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #164E3F (Teal-900)

**Status Badge (Bottom):**
- Same styling as full width version
- Font: Urbanist, 10px (text-[10px])

---

#### Size Variants

| Feature | Compact (10px) | Medium (12px) | Large (14px) |
|---------|----------------|---------------|--------------|
| Header Font | 10px | 12px | 14px |
| Cell Font Primary | 10px Semibold | 12px Semibold | 14px Semibold |
| Cell Font Secondary | 10px Normal | 12px Normal | 14px Normal |
| Row Padding | 10px (p-2.5) | 12px (p-3) | 16px (p-4) |
| Cell Gap | 2px (gap-0.5) | 4px (gap-1) | 6px (gap-1.5) |
| Sort Icon | 12px (w-3 h-3) | 16px (w-4 h-4) | 20px (w-5 h-5) |

---

#### Table States

**Row States:**

**Default:**
- Background: Transparent or #FFFFFF
- Border: 1px Neutral-200
- Text: Zinc-800 (primary), Neutral-500 (secondary)

**Hover:**
- Background: #F7F8F8 (Gray-BG Subtle)
- Border: 1px Neutral-300
- Cursor: pointer (if clickable)
- Transition: 150ms ease

**Selected:**
- Background: #E8F5FF (Blue-Subtle)
- Border: 1px Blue-300
- Left border: 3px Blue-500

**Disabled:**
- Background: Stone-50
- Text: Stone-400
- Cursor: not-allowed
- Opacity: 0.6

---

**Header States:**

**Default:**
- Text: Neutral-500
- Sort icons: Neutral-500 (both visible)
- Cursor: pointer (sortable columns)

**Hover:**
- Background: #FAFAFA (Neutral-50)
- Text: Zinc-700
- Transition: 150ms ease

**Sorted Ascending:**
- Up arrow: Teal-900 (active)
- Down arrow: Neutral-300 (inactive)
- Text: Zinc-800

**Sorted Descending:**
- Up arrow: Neutral-300 (inactive)
- Down arrow: Teal-900 (active)
- Text: Zinc-800

---

#### Responsive Behavior

**Desktop (1024px+):**
- Full table with all columns
- 5-7 columns visible
- Font: 10px or 12px
- Row padding: 10px

**Tablet (768px):**
- Hide less important columns (Note)
- 3-5 columns visible
- Horizontal scroll if needed
- Font: 10px

**Mobile (320px):**
- Compact layout (3 columns max)
- Stack amount + status
- Font: 12px for readability
- Consider card view instead

---

#### Table Features

**Sorting:**
- Click header to sort
- Toggle ascending/descending
- Visual indicator (arrows)
- Keyboard: Tab to header, Enter to sort

**Filtering:**
- Filter inputs in header row
- Search across all columns
- Date range pickers
- Status dropdown filters

**Pagination:**
- Show 10/20/50/100 rows per page
- Page controls at bottom
- Total count: "Showing 1-20 of 320"

**Selection:**
- Checkbox column (left)
- Select all checkbox in header
- Bulk actions toolbar
- Selected count indicator

**Row Actions:**
- Hover menu (right side)
- Context menu (right-click)
- Action buttons (Edit, Delete, View)
- Keyboard: Enter to expand

---

#### Best Practices

**Data Display:**
- Use consistent date/time formats
- Format numbers with appropriate decimals
- Truncate long text with ellipsis
- Provide tooltips for truncated content
- Color-code amounts (positive green, negative red)

**Column Sizing:**
- Fixed width for dates, amounts, status
- Flexible width for names, descriptions
- Minimum column width: 48px
- Resize columns drag handle

**Performance:**
- Virtualize for 100+ rows
- Lazy load data on scroll
- Cache sorted/filtered results
- Debounce search inputs

**Accessibility:**
- ARIA role: "table", "rowheader", "cell"
- ARIA sort: "ascending", "descending", "none"
- Keyboard navigation: Arrow keys to move, Tab to navigate
- Screen reader: announce column headers
- Focus indicators clearly visible
- High contrast mode support

---

#### Use Cases

**Transaction Table:**
```
┌────────────────────────────────────────────────┐
│ Name          Date        Amount    Status     │
├────────────────────────────────────────────────┤
│ Restaurant    2024-03-01  $226.25   Completed  │
│ Shopping      2024-03-02  $150.00   Pending    │
│ Transport     2024-03-03  $25.50    Completed  │
└────────────────────────────────────────────────┘
```

**User List:**
```
┌────────────────────────────────────────────────┐
│ Name          Email           Role      Status │
├────────────────────────────────────────────────┤
│ John Doe      john@mail.com   Admin    Active  │
│ Jane Smith    jane@mail.com   User     Active  │
└────────────────────────────────────────────────┘
```

**Product Inventory:**
```
┌────────────────────────────────────────────────┐
│ Product       SKU        Stock    Price        │
├────────────────────────────────────────────────┤
│ Widget A      WID-001    150      $25.00       │
│ Widget B      WID-002    75       $35.00       │
└────────────────────────────────────────────────┘
```

---

#### Advanced Table Patterns

**With Expandable Rows:**
```
┌────────────────────────────────────────────────┐
│ [▼] Order #123    2024-03-01   $500   Shipped │
│     └─ Item 1: Widget ($250)                   │
│     └─ Item 2: Gadget ($250)                   │
│ [▶] Order #124    2024-03-02   $300   Pending │
└────────────────────────────────────────────────┘
```

**With Inline Editing:**
```
┌────────────────────────────────────────────────┐
│ Name          [Edit inline]  Price    [Save]  │
├────────────────────────────────────────────────┤
│ Widget A      [  Widget A  ] $25.00   [✓]     │
└────────────────────────────────────────────────┘
```

**With Grouping:**
```
┌────────────────────────────────────────────────┐
│ March 2024                                     │
│   Restaurant    03-01    $226.25   Completed   │
│   Shopping      03-02    $150.00   Pending     │
│ February 2024                                  │
│   Transport     02-28    $25.50    Completed   │
└────────────────────────────────────────────────┘
```

---

#### Responsive Table Layouts

Адаптивные версии таблиц для разных разрешений экранов с оптимизированными колонками и улучшенной читабельностью.

---

##### Medium Width Table (836px)

**Container:**
- **Width**: 836px (w-[836px])
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-start
- **Gap**: 0 (no gap between rows)

**Header Row:**
- **Padding**: 16px/12px (px-4 py-3)
- **Background**: #F5F5F4 (Stone-100, bg-stone-100)
- **Border Radius**: 8px (rounded-lg) - only on header
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 10px (gap-2.5)

**Header Cell:**
- **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal)
- **Color**: #737373 (Neutral-500)
- **Sort Icon**: 12×12px (w-3 h-3), dual arrows
- **Cursor**: pointer (for sortable columns)

**Data Row:**
- **Padding**: 16px (p-4)
- **Background**: Transparent
- **Border Top**: 1px solid #E5E5E5 (Neutral-200, border-t border-neutral-200)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 10px (gap-2.5)

**Column Structure (with Checkbox):**

1. **Checkbox Column:**
   - Width: 12px (w-3)
   - Checkbox: 12×12px, same styling as full table

2. **Transaction Name:**
   - Width: 160px (w-40)
   - Font: Urbanist, 12px (text-xs), Weight 600 (Semibold), Zinc-800
   - Icon: 28×28px (if present)

3. **Transaction ID:**
   - Width: 80px (w-20)
   - Font: Urbanist, 12px (text-xs), Weight 400 (Normal), Neutral-500

4. **Date & Time:**
   - Width: 64px (w-16)
   - Font: Urbanist, 12px (text-xs), Weight 400 (Normal), Neutral-500

5. **Amount:**
   - Width: 48px (w-12)
   - Font: Urbanist, 12px (text-xs), Weight 600 (Semibold)
   - Color: Red-500 (#EF4444) for expenses, Emerald-500 (#10B981) for income

6. **Note:**
   - Width: 192px (w-48)
   - Font: Urbanist, 12px (text-xs), Weight 400 (Normal), Neutral-500
   - Text Overflow: line-clamp-2

7. **Status:**
   - Width: 80px (w-20)
   - Status badge with same styling as full table

**Key Features:**
- **Improved Readability**: 12px font (text-xs) throughout instead of 10px
- **Enhanced Header**: Stone-100 background with rounded corners
- **Consistent Padding**: 16px padding for better spacing
- **All Columns Visible**: Maintains checkbox + 6 data columns

---

##### Tablet Width Table (640px)

**Container:**
- **Width**: 640px (w-[640px])
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-start
- **Gap**: 0

**Header Row:**
- **Padding**: 14px/12px (px-3.5 py-3)
- **Background**: #F5F5F4 (Stone-100, bg-stone-100)
- **Border Radius**: 8px (rounded-lg)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 10px (gap-2.5)

**Header Cell:**
- **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal)
- **Color**: #737373 (Neutral-500)
- **Sort Icon**: 12×12px (w-3 h-3), dual arrows

**Data Row:**
- **Padding**: 14px (p-3.5)
- **Background**: Transparent
- **Border Top**: 1px solid #E5E5E5 (Neutral-200)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 10px (gap-2.5)

**Column Structure (Optimized for Tablet):**

1. **Transaction Name:**
   - Width: 176px (w-44)
   - Font: Urbanist, 12px (text-xs), Weight 600 (Semibold), Zinc-800
   - Icon: 28×28px circular with category background

2. **Combined Category + ID:**
   - Width: 144px (w-36)
   - Font: Urbanist, 12px (text-xs), Weight 400 (Normal), Neutral-500
   - Format: "Category - ID" (e.g., "Food & Dining - 4567890123")
   - Separator: " - " (space dash space)
   - Single line display

3. **Date & Time:**
   - Width: 64px (w-16)
   - Font: Urbanist, 12px (text-xs), Weight 400 (Normal), Neutral-500

4. **Amount:**
   - Width: 48px (w-12)
   - Font: Urbanist, 12px (text-xs), Weight 600 (Semibold)
   - Color: Red-500 or Emerald-500

5. **Note:**
   - Width: 128px (w-32)
   - Font: Urbanist, 12px (text-xs), Weight 400 (Normal), Neutral-500
   - Text Overflow: line-clamp-2

6. **Status:**
   - Width: 80px (w-20)
   - Status badge with same styling

**Key Features:**
- **Space Optimization**: Combined Category + ID into single column to save horizontal space
- **Reduced Note Width**: 128px instead of 192px for better fit
- **Maintained Readability**: 12px font throughout
- **No Checkbox**: Removed to fit more essential data
- **Stone-100 Header**: Background for visual separation

---

##### Responsive Layout Comparison

| Feature | Full Width (1139px) | Medium (836px) | Tablet (640px) |
|---------|---------------------|----------------|----------------|
| Checkbox | ✓ | ✓ | ✗ |
| Transaction Name | 160px | 160px | 176px |
| Category | Separate | Separate | Combined with ID |
| Transaction ID | 80px | 80px | Combined |
| Date & Time | 64px | 64px | 64px |
| Amount | 48px | 48px | 48px |
| Note | 192px | 192px | 128px |
| Status | 80px | 80px | 80px |
| Font Size | 10px/12px | 12px | 12px |
| Row Padding | 10px | 16px | 14px |
| Header BG | Transparent | Stone-100 | Stone-100 |

---

##### Responsive Table Best Practices

**Medium Width (836px):**
- Use when displaying on tablets in landscape mode or medium desktop windows
- Prioritize readability with 12px font
- Maintain all essential columns including checkbox for bulk actions
- Stone-100 header background improves visual hierarchy

**Tablet Width (640px):**
- Optimal for tablets in portrait mode or small desktop windows
- Combine related fields (Category + ID) to save space
- Remove checkbox if bulk actions are not critical
- Reduce Note column width but maintain line-clamp-2 for context
- Keep 12px font for comfortable reading on smaller screens

**Data Combination Patterns:**
- **Category + ID**: "Food & Dining - 4567890123" (separator: " - ")
- **Date + Time**: Can be combined in single column if space is critical
- **Amount + Status**: Stack vertically if horizontal space is limited

**Layout Adaptation:**
- **From Full to Medium**: Remove checkbox if needed, increase padding for touch targets
- **From Medium to Tablet**: Combine Category + ID, reduce Note width, remove checkbox
- **From Tablet to Mobile**: Switch to card-based layout (see Compact Layout section)

**Accessibility Considerations:**
- Maintain minimum 44×44px touch targets on tablet devices
- Ensure combined fields have clear separators for screen readers
- ARIA labels should describe combined fields: "Category and Transaction ID"
- Header sort icons remain 12×12px minimum for visibility

---

##### Narrow Table (770px) - Inline Layout

**Container:**
- **Width**: 770px (w-[770px])
- **Padding**: 20px (p-5)
- **Border**: 1px solid #A855F7 (Purple-500) - for container demo
- **Border Radius**: 5px (rounded-[5px])
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-start
- **Gap**: 20px (gap-5)
- **Overflow**: Hidden

**Header Row:**
- **Padding Left**: 16px (pl-4)
- **Padding Vertical**: 12px (py-3)
- **Background**: #F5F5F4 (Stone-100, bg-stone-100)
- **Border Radius**: Not specified (inline-flex)
- **Display**: Inline-flex
- **Alignment**: justify-between, items-center

**Header Cell:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal)
- **Color**: #737373 (Neutral-500)
- **Line Height**: 12px (leading-3)
- **Sort Icon**: 12×12px (w-3 h-3), dual arrows

**Data Row:**
- **Padding Left**: 16px (pl-4)
- **Padding Vertical**: 16px (py-4)
- **Background**: Transparent
- **Border Top**: 1px solid #E5E5E5 (Neutral-200)
- **Display**: Inline-flex
- **Alignment**: justify-between, items-center

**Column Structure (4 columns):**

1. **Transaction Type (Horizontal Inline):**
   - Width: 176px (w-44)
   - Display: Flex, justify-start, items-center
   - Gap: 10px (gap-2.5)
   - **Icon Container**: 6px padding (p-1.5), Lime-200, rounded-[56px]
   - **Icon**: 12×12px (w-3 h-3), Zinc-800
   - **Text Layout**: Horizontal inline with separator
     - **Type**: Urbanist 12px Medium, Zinc-800
     - **Separator**: " - " (dash with spaces)
     - **Name**: Urbanist 12px Normal, Neutral-500
   - Format: "Withdraw - Andrew Forbist"

2. **Date & Time (Horizontal Inline):**
   - Width: 112px (w-28)
   - Display: Flex, justify-start, items-baseline
   - Gap: 4px (gap-1)
   - **Date**: Urbanist 12px Normal, Zinc-800
   - **Separator**: " - " (dash with spaces, Neutral-500)
   - **Time**: Urbanist 12px Normal, Neutral-500
   - Format: "2024-09-24 - 14:30"

3. **Amount:**
   - Width: 48px (w-12)
   - Display: Flex, justify-start, items-center
   - Gap: 4px (gap-1)
   - **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal)
   - **Color**: Teal-900 (#164E3F) for positive, Red-500 for negative
   - Format: "+$64" or "-$64"

4. **Brief Note:**
   - Width: 176px (w-44)
   - Display: Flex, justify-start, items-center
   - Gap: 6px (gap-1.5)
   - **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal), Zinc-800
   - **Text Overflow**: line-clamp-2
   - Example: "Added extra savings from bonus"

**Key Features:**
- **Horizontal Inline Layout**: Type and Name displayed on same line with dash separator
- **Date & Time Inline**: Date and time on same line with dash separator
- **4 Columns Only**: Transaction Type, Date & Time, Amount, Brief Note
- **Clean Separators**: Uses " - " (space-dash-space) for readability
- **No Checkbox or Status**: Simplified for narrow display

---

##### Mobile Table (384px) - Vertical Stack Layout

**Container:**
- **Width**: 384px (w-96)
- **Padding**: 20px (p-5)
- **Border**: 1px solid #A855F7 (Purple-500)
- **Border Radius**: 5px (rounded-[5px])
- **Display**: Inline-flex, flex-col
- **Gap**: 20px (gap-5)
- **Overflow**: Hidden

**Header Row:**
- **Padding Left**: 10px (pl-2.5)
- **Padding Vertical**: 12px (py-3)
- **Background**: #F5F5F4 (Stone-100, bg-stone-100)
- **Border Radius**: Not specified (inline-flex)
- **Display**: Inline-flex
- **Alignment**: justify-between, items-center

**Header Cell:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal)
- **Color**: #737373 (Neutral-500)
- **Line Height**: 12px (leading-3)
- **Sort Icon**: 12×12px (w-3 h-3), dual arrows

**Data Row:**
- **Padding Left**: 10px (pl-2.5)
- **Padding Vertical**: 16px (py-4)
- **Background**: Transparent
- **Border Top**: 1px solid #E5E5E5 (Neutral-200)
- **Display**: Inline-flex
- **Alignment**: justify-between, items-center

**Column Structure (4 columns with vertical stacking):**

1. **Transaction Type (Vertical Stack):**
   - Width: 112px (w-28)
   - Display: Flex, justify-start, items-center
   - Gap: 8px (gap-2)
   - **Icon Container**: 6px padding (p-1.5), Lime-200, rounded-[56px]
   - **Icon**: 12×12px (w-3 h-3), Zinc-800
   - **Text Layout**: Vertical stack (inline-flex, flex-col)
     - Gap: 2px (gap-0.5)
     - **Type (Top)**: Urbanist 12px Medium, Zinc-800, leading-4
     - **Name (Bottom)**: Urbanist 12px Normal, Neutral-500, leading-4
   - Format:
     ```
     Withdraw
     Andrew Forbist
     ```

2. **Date & Time (Vertical Stack):**
   - Width: 64px (w-16)
   - Display: Inline-flex, flex-col, justify-center, items-start
   - Gap: 2px (gap-0.5)
   - **Date (Top)**: Urbanist 12px Normal, Zinc-800, leading-4
   - **Time (Bottom)**: Urbanist 12px Normal, Neutral-500, leading-4
   - Format:
     ```
     2024-09-24
     14:30
     ```

3. **Amount:**
   - Width: 48px (w-12)
   - Display: Flex, **justify-center**, items-center
   - Gap: 4px (gap-1)
   - **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal)
   - **Color**: Teal-900 (#164E3F) for positive, Red-500 for negative
   - **Alignment**: Center-aligned (justify-center)
   - Format: "+$64"

4. **Brief Note:**
   - Width: 128px (w-32)
   - Display: Flex, justify-start, items-center
   - Gap: 6px (gap-1.5)
   - **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal), Zinc-800
   - **Line Height**: 16px (leading-4)
   - **Text Overflow**: line-clamp-2
   - **Flex**: flex-1 (takes available space)
   - Example: "Added extra savings from bonus"

**Key Features:**
- **Vertical Stack Layout**: Transaction Type and Date & Time displayed as stacked elements
- **Space Saving**: 2px gap (gap-0.5) between stacked items for compact display
- **Center-Aligned Amount**: Amount column uses justify-center for better visual balance
- **Reduced Padding**: 10px left padding (pl-2.5) instead of 16px
- **Mobile Optimized**: 384px width perfect for mobile devices
- **No Separators**: Vertical stacking replaces inline separators for cleaner mobile view

---

##### Narrow Table Layout Comparison

| Feature | Narrow (770px) | Mobile (384px) |
|---------|----------------|----------------|
| Container Padding | 20px (p-5) | 20px (p-5) |
| Header Padding Left | 16px (pl-4) | 10px (pl-2.5) |
| Row Padding Left | 16px (pl-4) | 10px (pl-2.5) |
| Transaction Type Width | 176px (w-44) | 112px (w-28) |
| Transaction Layout | Horizontal inline | Vertical stack |
| Date & Time Width | 112px (w-28) | 64px (w-16) |
| Date Layout | Horizontal inline | Vertical stack |
| Amount Width | 48px | 48px |
| Amount Alignment | justify-start | justify-center |
| Brief Note Width | 176px (w-44) | 128px (w-32) |
| Stack Gap | N/A | 2px (gap-0.5) |
| Inline Separator | " - " | N/A |

---

##### Narrow Table Layout Patterns

**When to Use Horizontal Inline (770px):**
- Small desktop windows or tablet landscape mode
- When horizontal space allows inline text
- For maintaining familiar left-to-right reading flow
- When separator " - " provides clear visual separation

**When to Use Vertical Stack (384px):**
- Mobile devices or very narrow containers
- When horizontal space is extremely limited
- For better readability on small screens
- When vertical scrolling is preferred over horizontal

**Transition Strategy:**
- **640px → 770px**: Remove combined Category+ID, use horizontal inline for Type and Date
- **384px → 640px**: Switch from vertical stack to horizontal inline or combined fields
- **Below 384px**: Consider switching to card-based layout entirely

**Data Display Patterns:**

**Horizontal Inline Format:**
```
Type - Name       Date - Time
Withdraw - Andrew Forbist    2024-09-24 - 14:30
```

**Vertical Stack Format:**
```
Type              Date
Name              Time

Withdraw          2024-09-24
Andrew Forbist    14:30
```

**Mobile Layout Best Practices:**
- Use 2px gap (gap-0.5) for compact vertical stacking
- Center-align numerical values (Amount) for visual balance
- Reduce horizontal padding to 10px (pl-2.5) to maximize content space
- Maintain 12px font size for readability on small screens
- Use line-clamp-2 for notes to prevent excessive height
- Keep icon sizes at 12×12px minimum for touch targets

---

#### Invoice Tables

Специализированные таблицы для отображения инвойсов и счетов с поддержкой разных разрешений экранов.

---

##### Invoice Table - Full Width (1139px)

**Container:**
- **Width**: 1139px (w-[1139px])
- **Padding**: 20px (p-5)
- **Border**: 1px solid #A855F7 (Purple-500) - for demo container
- **Border Radius**: 5px (rounded-[5px])
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-start
- **Gap**: 20px (gap-5)
- **Overflow**: Hidden

**Header Row:**
- **Width**: 1139px (w-[1139px])
- **Padding Horizontal**: 24px (px-6)
- **Padding Vertical**: 16px (py-4)
- **Background**: #F5F5F4 (Stone-100, bg-stone-100)
- **Display**: Inline-flex
- **Alignment**: justify-start, items-center
- **Gap**: 20px (gap-5)

**Header Structure:**
1. **Checkbox**: 12×12px (w-3 h-3), Neutral-50 bg, Stone-200 outline
2. **Flex-1 Container**: Contains all column headers with justify-between
3. **Action Column Space**: 24px (w-6) reserved for action menu

**Header Columns:**
- **Invoice Name**: 192px (w-48)
- **Invoice ID**: 80px (w-20)
- **Total Amount**: 64px (w-16)
- **Date & Time**: 176px (w-44)
- **Status**: 64px (w-16)
- **Actions Space**: 24px (w-6, h-3) - empty spacer

**Header Cell:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400 (Normal)
- **Color**: #737373 (Neutral-500)
- **Line Height**: 12px (leading-3)
- **Sort Icon**: 12×12px (w-3 h-3), dual arrows (4×2.62px each)

---

**Data Row:**
- **Width**: 1139px (w-[1139px])
- **Padding Horizontal**: 24px (px-6)
- **Padding Vertical**: 16px (py-4)
- **Background**: Transparent
- **Border Bottom**: 1px solid #E5E5E5 (Neutral-200, border-b border-neutral-200)
- **Display**: Inline-flex
- **Alignment**: justify-start, items-center
- **Gap**: 20px (gap-5)

**Data Row Structure:**
1. **Checkbox**: 12×12px (w-3 h-3), Neutral-100 bg, Stone-200 outline
2. **Flex-1 Container**: Contains all data cells with justify-between
3. **Action Button**: 16×16px (w-4 h-4) icon

**Data Columns:**

1. **Invoice Name:**
   - Width: 192px (w-48)
   - Display: Flex, justify-start, items-center
   - Gap: 10px (gap-2.5)
   - **Icon Container**: 28×28px (w-7 h-7), Lime-200, rounded-[56px], overflow-hidden
   - **Icon**: 12×12px (w-3 h-3), Zinc-800, positioned at left-[7px] top-[7px]
   - **Text**: Urbanist 12px Medium, Zinc-800, leading-4
   - Example: "Annual Software Subscription"

2. **Invoice ID:**
   - Width: 80px (w-20)
   - Display: Inline-flex, flex-col, justify-center, items-start
   - **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal), Zinc-800
   - **Line Height**: 16px (leading-4)
   - Format: "INV-281005-001"

3. **Total Amount:**
   - Width: 64px (w-16)
   - Display: Flex, justify-start, items-center
   - Border Radius: 8px (rounded-lg) - container only
   - **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal)
   - **Color**: #164E3F (Teal-900)
   - **Line Height**: 16px (leading-4)
   - Format: "$350.00"

4. **Date & Time (Horizontal Inline):**
   - Width: 176px (w-44)
   - Display: Flex, justify-start, items-start
   - Gap: 4px (gap-1)
   - **Date**: Urbanist 12px Normal, Zinc-800, leading-4
   - **Separator**: " - " (dash, Neutral-500)
   - **Time**: Urbanist 12px Normal, Neutral-500, leading-4
   - Format: "September 24, 2028 - 08.30 AM"

5. **Status:**
   - Width: 64px (w-16)
   - Display: Inline-flex, flex-col, justify-center, items-start
   - **Badge Container**: px-2.5 py-1, rounded-2xl
     - **Overdue**: Rose-200 bg (#FFE4E6), Red-500 text (#EF4444)
     - **Paid**: Emerald-200 bg, Emerald-500 text
     - **Pending**: Yellow-200 bg, Yellow-900 text
   - **Text**: Urbanist 12px Normal, leading-4
   - data-state attribute: "Overdue", "Paid", "Pending"

6. **Action Button:**
   - Width: 24px (w-6)
   - Display: Inline-flex, flex-col, justify-center, items-start
   - **Button**: 3px padding (p-[3px]), rounded-[5px]
   - **Icon**: 16×16px (w-4 h-4), Teal-900 (menu icon - 3 dots)
   - data-type: "Transparent"
   - data-size: "xSmall"
   - data-show-badge: "true"

**Key Features:**
- **Full Data Set**: All columns visible including action menu
- **Horizontal Date Layout**: Date and time on same line for space efficiency
- **Action Menu**: 3-dot menu icon for row actions (view, edit, delete)
- **Large Padding**: 24px horizontal padding (px-6) for desktop comfort
- **Icon Indicators**: 28×28px circular icons for visual recognition

---

##### Invoice Table - Medium Width (672px)

**Container:**
- **Width**: 672px (w-[672px])
- **Padding**: 20px (p-5)
- **Border**: 1px solid #A855F7 (Purple-500)
- **Border Radius**: 5px (rounded-[5px])
- **Display**: Inline-flex, flex-col
- **Gap**: 20px (gap-5)
- **Overflow**: Hidden

**Header Row:**
- **Width**: 672px (w-[672px])
- **Padding Horizontal**: 16px (px-4)
- **Padding Vertical**: 14px (py-3.5)
- **Background**: #F5F5F4 (Stone-100, bg-stone-100)
- **Display**: Inline-flex
- **Alignment**: justify-start, items-center
- **Gap**: 16px (gap-4)

**Header Structure:**
1. **Checkbox**: 12×12px (w-3 h-3)
2. **Flex-1 Container**: Contains all column headers with justify-between
3. **No Action Column**: Action menu removed to save space

**Header Columns:**
- **Invoice Name**: 192px (w-48)
- **Invoice ID**: 80px (w-20)
- **Total Amount**: 64px (w-16)
- **Date & Time**: 112px (w-28) - reduced from 176px
- **Status**: 64px (w-16)

**Header Cell:**
- Same styling as full width version
- Font: Urbanist 10px Normal, Neutral-500

---

**Data Row:**
- **Width**: 672px (w-[672px])
- **Padding**: 16px (p-4)
- **Background**: Transparent
- **Border Bottom**: 1px solid #E5E5E5 (Neutral-200)
- **Display**: Inline-flex
- **Alignment**: justify-start, items-center
- **Gap**: 16px (gap-4)

**Data Row Structure:**
1. **Checkbox**: 12×12px (w-3 h-3)
2. **Flex-1 Container**: Contains all data cells with justify-between
3. **No Action Button**: Removed for space optimization

**Data Columns:**

1. **Invoice Name:**
   - Width: 192px (w-48)
   - Same styling as full width
   - Icon: 28×28px, Lime-200
   - Text: Urbanist 12px Medium, Zinc-800

2. **Invoice ID:**
   - Width: 80px (w-20)
   - Same styling as full width
   - Format: "INV-281005-001"

3. **Total Amount:**
   - Width: 64px (w-16)
   - Display: Flex, **justify-center**, items-center
   - Border Radius: 8px (rounded-lg)
   - **Font**: Urbanist 12px Normal, Teal-900
   - **Center-Aligned**: justify-center for visual balance
   - Format: "$350.00"

4. **Date & Time (Vertical Stack):**
   - Width: 112px (w-28)
   - Display: Inline-flex, flex-col, justify-start, items-start
   - Gap: 2px (gap-0.5)
   - **Date (Top)**: Urbanist 12px Normal, Zinc-800, leading-4
   - **Time (Bottom)**: Urbanist 12px Normal, Neutral-500, leading-4
   - Format:
     ```
     September 24, 2028
     08.30 AM
     ```

5. **Status:**
   - Width: 64px (w-16)
   - Same badge styling as full width
   - Rose-200 bg, Red-500 text for "Overdue"

**Key Features:**
- **No Action Menu**: Removed to fit medium screen width
- **Vertical Date Stack**: Date and time stacked to save horizontal space
- **Center-Aligned Amount**: Better visual balance in narrower layout
- **Reduced Padding**: 16px horizontal padding (px-4) instead of 24px
- **Compact Gap**: 16px gap (gap-4) instead of 20px

---

##### Invoice Table Layout Comparison

| Feature | Full Width (1139px) | Medium (672px) |
|---------|---------------------|----------------|
| Container Padding | 20px (p-5) | 20px (p-5) |
| Header Padding Horizontal | 24px (px-6) | 16px (px-4) |
| Header Padding Vertical | 16px (py-4) | 14px (py-3.5) |
| Row Padding | 24px (px-6, py-4) | 16px (p-4) |
| Row Gap | 20px (gap-5) | 16px (gap-4) |
| Checkbox | ✓ | ✓ |
| Invoice Name | 192px | 192px |
| Invoice ID | 80px | 80px |
| Total Amount | 64px (left-aligned) | 64px (center-aligned) |
| Date & Time | 176px (horizontal) | 112px (vertical) |
| Status | 64px | 64px |
| Action Menu | ✓ (24px) | ✗ |
| Date Layout | Inline with " - " | Vertical stack |
| Amount Alignment | justify-start | justify-center |

---

##### Invoice Table Status Variants

**Status Badge States:**

**Overdue:**
- Background: #FFE4E6 (Rose-200, bg-rose-200)
- Text: #EF4444 (Red-500)
- Padding: 10px/4px (px-2.5 py-1)
- Border Radius: 16px (rounded-2xl)
- data-state: "Overdue"

**Paid:**
- Background: #A7F3D0 (Emerald-200)
- Text: #10B981 (Emerald-500)
- Same padding and border radius

**Pending:**
- Background: #FEF08A (Yellow-200)
- Text: #713F12 (Yellow-900)
- Same padding and border radius

**Draft:**
- Background: #E5E5E5 (Neutral-200)
- Text: #737373 (Neutral-500)
- Same padding and border radius

**Cancelled:**
- Background: #FED7AA (Orange-200)
- Text: #EA580C (Orange-600)
- Same padding and border radius

---

##### Invoice Table Best Practices

**Full Width (1139px):**
- Use for desktop displays and large screens
- Include action menu for quick access to row operations
- Horizontal date layout maintains single-line rows
- 24px padding provides comfortable spacing for mouse interaction

**Medium Width (672px):**
- Optimal for tablets and small desktop windows
- Remove action menu to prioritize data visibility
- Vertical date stack saves 64px horizontal space
- Center-align amount for better visual hierarchy
- 16px padding suitable for touch targets

**Data Display:**
- **Invoice Names**: Keep descriptive but concise (2-4 words)
- **Invoice IDs**: Use consistent format (INV-YYMMDD-XXX)
- **Amounts**: Always show currency symbol and 2 decimal places
- **Dates**: Use readable format (Month DD, YYYY) not shortened
- **Time**: Use 12-hour format with AM/PM

**Icon Usage:**
- 28×28px circular icons for invoice types
- Lime-200 default background
- Alternative colors by category:
  - Subscription: Lime-200
  - One-time: Blue-200
  - Recurring: Purple-200
  - Refund: Orange-200

**Interaction Patterns:**
- Checkbox for bulk selection and batch operations
- Click row to view invoice details
- Action menu (full width) for Edit, Download PDF, Send Email, Delete
- Hover state shows row background Stone-50
- Selected row shows Blue-50 background with left border

**Accessibility:**
- ARIA label for action button: "Invoice actions menu"
- Status badges use semantic colors with sufficient contrast
- Date format announced clearly by screen readers
- Keyboard navigation: Tab through checkboxes, Enter to open invoice

---

### 7. Navigation

#### Main Navigation

- **Height**: 64px
- **Background**: #FFFFFF
- **Shadow**: var(--shadow-sm)
- **Item Padding**: 12px 24px
- **States**:
  - Default: Color #333E47 (Gray-30)
  - Hover: Background #F7F8F8 (Gray-BG Subtle), Color #000E19 (Black)
  - Active: Color #3384C6 (Blue-00), Border-bottom 2px solid #3384C6

#### Sidebar Navigation

Полнофункциональная боковая навигация с поддержкой свернутого режима и мобильной версии.

---

##### Sidebar Container (Desktop - Full Width)

**Container:**
- **Width**: 192px (w-48)
- **Height**: 1034px (h-[1034px]) - full height example
- **Padding Horizontal**: 16px (px-4)
- **Padding Top**: 20px (pt-5)
- **Padding Bottom**: 24px (pb-6)
- **Background**: #F5F5F4 (Stone-100)
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-start
- **Gap**: 20px (gap-5)

**Layout Structure:**
1. Logo section (top)
2. Navigation items (middle, flex-1)
3. Promo/CTA card (bottom)

---

##### Logo Section

**Logo Container:**
- **Padding Horizontal**: 8px (px-2)
- **Display**: Flex, flex-col
- **Gap**: 10px (gap-2.5)

**Logo (Full Text):**
- **Width**: 128px (w-32)
- **Height**: 36px (h-9)
- **Position**: Relative
- **Contains**: Brand icon + text elements
- **Icon**: 20px × 20px (w-5 h-5), positioned at left-[8px], top-[8px]
- **Text**: Multiple text elements (Zinc-800), positioned absolutely

**Logo (Symbol Only - Collapsed):**
- **Width**: 20px (w-5)
- **Height**: Auto
- **Display**: Inline-flex, justify-center, items-center
- **Contains**: Only brand icon, no text

---

##### Navigation Items Section

**Items Container:**
- **Width**: 160px (w-40)
- **Flex**: 1 (flex-1) - takes remaining space
- **Display**: Flex, flex-col
- **Gap**: 8px (gap-2) between items

---

##### Navigation Item (Desktop - Active)

**Active Item:**
- **Full Width**: self-stretch
- **Padding Left**: 16px (pl-4)
- **Padding Right**: 12px (pr-3)
- **Padding Vertical**: 8px (py-2)
- **Background**: #ECFCCB (Lime-200)
- **Border Radius**: 24px (rounded-3xl)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 12px (gap-3)

**Icon Container:**
- **Size**: 24px × 24px (w-6 h-6)
- **Position**: Relative
- **Overflow**: Hidden

**Icon Graphic:**
- **Size**: 16px × 16px (w-4 h-4)
- **Position**: Absolute, left 3.75px, top 3.75px (centered)
- **Background**: #27272A (Zinc-800)

**Text Container:**
- **Padding Right**: 2px (pr-0.5)
- **Padding Vertical**: 5px (py-[5px])
- **Display**: Flex
- **Gap**: 10px (gap-2.5)

**Text:**
- **Font**: Urbanist, 14px (text-sm), Weight 600 (Semibold), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Alignment**: text-center justify-start

---

##### Navigation Item (Desktop - Inactive)

**Inactive Item:**
- **Full Width**: self-stretch
- **Padding Left**: 16px (pl-4)
- **Padding Right**: 4px (pr-1)
- **Padding Vertical**: 8px (py-2)
- **Background**: Transparent
- **Border Radius**: 24px (rounded-3xl)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 12px (gap-3)
- **Overflow**: Hidden

**Icon Graphic:**
- **Size**: Varies (16-24px depending on icon)
- **Background**: #737373 (Neutral-500)

**Text:**
- **Font**: Urbanist, 14px (text-sm), Weight 600 (Semibold), Line Height 16px (leading-4)
- **Color**: #737373 (Neutral-500)
- **Flex**: 1 (flex-1)

---

##### Navigation Item with Dropdown

**Dropdown Indicator:**
- **Padding Vertical**: 2px (py-0.5)
- **Display**: Flex
- **Gap**: 10px (gap-2.5)

**Arrow Icon:**
- **Size**: 14px × 14px (w-3.5 h-3.5)
- **Position**: Relative

**Arrow Graphic:**
- **Size**: 8px × 4px (w-2 h-1)
- **Position**: Absolute, left 3.06px, top 5.25px
- **Background**: #A3A3A3 (Neutral-400)
- **Direction**: Down (collapsed), Up (expanded)

---

##### Navigation Item with Badge

**Badge Container:**
- **Size**: 20px × 20px (w-5 h-5)
- **Padding**: 2px (p-0.5)
- **Display**: Inline-flex, flex-col
- **Alignment**: items-center, justify-center
- **Gap**: 10px (gap-2.5)

**Badge (with number):**
- **Size**: 16px × 16px (w-4 h-4)
- **Padding Horizontal**: 2px (px-0.5)
- **Background**: #EF4444 (Red-500)
- **Border Radius**: 10px (rounded-[10px])
- **Display**: Flex, flex-col
- **Alignment**: items-center, justify-center

**Badge Text:**
- **Font**: Urbanist, 12px (text-xs), Weight 400, Line Height 12px (leading-3)
- **Color**: #FAFAFA (Neutral-50)
- **Example**: "99", "5", "12"

**Badge (dot only):**
- **Size**: 10px × 10px (w-2.5 h-2.5)
- **Padding Horizontal**: 2px (px-0.5)
- **Background**: #EF4444 (Red-500)
- **Border Radius**: 10px (rounded-[10px])
- **Position**: Absolute, left-[18px], top-[2px] (for Tab version)

---

##### Promo Card (Bottom Section)

**Card Container:**
- **Height**: 208px (h-52)
- **Padding Horizontal**: 16px (px-4)
- **Padding Vertical**: 20px (py-5)
- **Background**: #164E3F (Teal-900)
- **Border Radius**: 16px (rounded-2xl)
- **Position**: Relative
- **Display**: Flex, flex-col
- **Alignment**: items-start, justify-end
- **Gap**: 20px (gap-5)
- **Overflow**: Hidden

**Icon Badge (Top Left):**
- **Size**: 32px × 32px (w-8 h-8)
- **Position**: Absolute, left-[17px], top-[16px]
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: 8px (rounded-lg)

**Icon Inside Badge:**
- **Size**: 16px × 16px (w-4 h-4)
- **Position**: Absolute, left-[7px], top-[7px] (centered in badge)
- **Icon Graphic**: 14px × 16px (w-3.5 h-4), Teal-900

**Description Text:**
- **Width**: 128px (w-32)
- **Font**: Urbanist, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
- **Color**: #F5F5F4 (Stone-100)
- **Example**: "Gain full access to your finances with detailed analytics and graphs"

**CTA Button:**
- **Padding Horizontal**: 14px (px-3.5)
- **Padding Vertical**: 10px (py-2.5)
- **Background**: #ECFCCB (Lime-200)
- **Border Radius**: 8px (rounded-lg)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-center

**Button Text:**
- **Font**: Urbanist, 14px (text-sm), Weight 500 (Medium), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Example**: "Get Pro", "Upgrade"

**Background Decoration:**
- **Size**: 64px × 64px (w-16 h-16)
- **Position**: Absolute, left-[95px], top-[-8px]
- **Opacity**: 0.2 (opacity-20)
- **Use case**: Decorative background element

---

##### Sidebar Collapsed/Tab Version

**Container:**
- **Height**: 1034px (h-[1034px])
- **Padding Horizontal**: 16px (px-4)
- **Padding Top**: 20px (pt-5)
- **Padding Bottom**: 24px (pb-6)
- **Background**: #F5F5F4 (Stone-100)
- **Display**: Inline-flex, flex-col
- **Gap**: 20px (gap-5)
- **Width**: Auto (shrinks to icon size)

**Logo (Symbol Only):**
- **Padding**: 8px (p-2)
- **Size**: 20px (w-5) icon only

**Navigation Item (Active - Tab):**
- **Padding**: 8px (p-2)
- **Background**: #ECFCCB (Lime-200)
- **Border Radius**: 24px (rounded-3xl)
- **Display**: Inline-flex
- **Gap**: 12px (gap-3)
- **Size**: 40px × 40px total

**Navigation Item (Inactive - Tab):**
- **Padding**: 8px (p-2)
- **Background**: Transparent
- **Border Radius**: 24px (rounded-3xl)
- **Icon**: 24px × 24px, Neutral-500

**Badge Position (Tab Version):**
- **Position**: Absolute, left-[18px], top-[2px]
- **Shows as dot** (10px × 10px) instead of number
- **Background**: Red-500

**No Promo Card** in collapsed version

---

##### Mobile Top Bar Version

**Container:**
- **Width**: 384px (w-96) or full width
- **Padding**: 16px (p-4)
- **Background**: #F5F5F4 (Stone-100)
- **Display**: Flex
- **Alignment**: items-center, justify-between
- **Layout**: Horizontal (Logo | Title | Menu Icon)

**Logo (Left):**
- **Padding**: 8px (p-2)
- **Size**: 20px (w-5) symbol only

**Page Title (Center):**
- **Font**: Urbanist, 20px (text-xl), Weight 700 (Bold), Line Height 28px (leading-7)
- **Color**: #164E3F (Teal-900)
- **Example**: "Dashboard", "Payments"

**Menu Button (Right):**
- **Padding**: 5px (p-[5px])
- **Border Radius**: 6px (rounded-md)
- **Display**: Flex
- **Gap**: 8px (gap-2)

**Menu Icon:**
- **Size**: 20px × 20px (w-5 h-5)
- **Icon Graphic**: 16px × 12px (w-4 h-3), Teal-900
- **Use case**: Hamburger menu or notification icon

---

##### States & Interactions

**Navigation Item States:**

**Default (Inactive):**
- Background: Transparent
- Icon: Neutral-500 (#737373)
- Text: Neutral-500 (#737373)
- Font Weight: 600 (Semibold)

**Hover:**
- Background: #FAFAFA (Neutral-50) or #E7E5E4 (Stone-200)
- Icon: Zinc-800
- Text: Zinc-800
- Cursor: pointer
- Transition: 150ms ease

**Active/Selected:**
- Background: Lime-200 (#ECFCCB)
- Icon: Zinc-800 (#27272A)
- Text: Zinc-800 (#27272A)
- Font Weight: 600 (Semibold)

**Pressed:**
- Background: Lime-300 (slightly darker)
- Scale: 0.98

**Disabled:**
- Background: Transparent
- Icon: Stone-300
- Text: Stone-300
- Opacity: 0.5
- Cursor: not-allowed

**Focus:**
- Outline: 2px solid Teal-900
- Outline offset: 2px

---

**Dropdown States:**
- **Collapsed**: Arrow down, no submenu visible
- **Expanded**: Arrow up, submenu visible below
- **Submenu Items**: Indented 32px, smaller font (12px)

---

##### Best Practices

**Navigation Structure:**
- Group related items together
- Use clear, concise labels (1-2 words)
- Limit to 7-10 main items
- Use icons that clearly represent sections
- Place most important items at top
- Settings/profile items at bottom

**Responsive Behavior:**
- **Desktop (1024px+)**: Full sidebar with text
- **Tablet (768px)**: Collapsed sidebar (icons only)
- **Mobile (320px)**: Top bar with hamburger menu

**Badge Usage:**
- Show number badge for counts up to 99, then "99+"
- Use dot badge for binary states (has notifications/doesn't)
- Position badges consistently (top-right of icon)
- Update in real-time for notifications

**Promo Card:**
- Keep text concise (max 2 lines)
- Use clear CTA text
- Contrast colors for visibility
- Optional, can be hidden or replaced

**Accessibility:**
- ARIA role: "navigation" for container
- ARIA current: "page" for active item
- ARIA expanded: for dropdown items
- Keyboard navigation: Tab to focus, Enter to select, Arrow keys to navigate
- Focus indicators clearly visible
- Screen reader: announce item labels and states
- Skip navigation link for keyboard users
- Minimum touch target: 40px × 40px

**Performance:**
- Lazy load dropdown submenus
- Cache navigation state
- Smooth collapse/expand animations
- Debounce hover states

---

##### Layout Patterns

**Full Sidebar (Desktop):**
```
┌────────────────┐
│ [LOGO]         │
├────────────────┤
│ ● Dashboard    │ ← Active
│ ○ Payments  ▼  │ ← Dropdown
│ ○ Transactions │
│ ○ Invoices     │
│ ○ Cards        │
│ ○ Investments  │
│ ○ Inbox     [5]│ ← Badge
│ ○ Promos       │
│ ○ Insights     │
├────────────────┤
│ [Promo Card]   │
│ Get Pro →      │
└────────────────┘
```

**Collapsed Sidebar (Tablet):**
```
┌──┐
│ ◉│ ← Logo
├──┤
│●│ ← Active
│○│
│○│
│○│
│○│
│○│
│◎│ ← Badge
│○│
│○│
└──┘
```

**Mobile Top Bar:**
```
┌────────────────────────┐
│ ◉  Dashboard    ≡     │
└────────────────────────┘
```

---

#### Breadcrumb Navigation

- **Font**: Lato, 12px (0.75rem / text-xs), Weight 400 (Normal), Line Height 16px (leading-4)
- **Gap between items**: 6px (gap-1.5)
- **Separator**: "/" (forward slash)
- **Colors**:
  - Link (inactive): #A1A1AA (Zinc-400)
  - Separator: #E4E4E7 (Zinc-200)
  - Current page: #A1A1AA (Zinc-400) or #000E19 (Black) for emphasis
- **States**:
  - Link Hover: Color #3384C6 (Blue-00), Underline
  - Link Active: Color #000E19 (Black)
  - Current page (non-clickable): Color #000E19 (Black), No hover effect
- **Structure**: Link / Link / Current Page

**Пример:**
```
Home / Products / Category / Current Page
```

---

#### Pagination

Компонент навигации по страницам для таблиц, списков и результатов поиска.

---

##### Pagination Container

**Container:**
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 8px (gap-2) between elements
- **Layout**: Horizontal row

**Elements Order:**
1. Previous button (left arrow)
2. Page numbers (1, 2, 3, ...)
3. Ellipsis (...)
4. Last page number
5. Next button (right arrow)

---

##### Pagination - Small Size

**Container Gap:** 8px (gap-2)

**Previous/Next Button:**
- **Padding**: 6px (p-1.5)
- **Background**: #F4F4F5 (Zinc-100) - disabled, #F5F5F4 (Stone-100) - enabled
- **Border Radius**: 6px (rounded-md)
- **Display**: Flex
- **Gap**: 8px (gap-2)

**Arrow Icon Container:**
- **Size**: 14px × 14px (w-3.5 h-3.5)
- **Position**: Relative

**Arrow Graphic:**
- **Size**: 8px × 4px (w-2 h-1)
- **Position**: Absolute
- **Previous Arrow**: left 4.38px, top 10.94px, rotate -90deg
- **Next Arrow**: left 5.25px, top 10.94px, rotate -90deg
- **Color (Disabled)**: #D6D3D1 (Stone-300)
- **Color (Enabled)**: #27272A (Zinc-800)

**Page Number Button (Active):**
- **Width**: 28px (w-7)
- **Padding Horizontal**: 10px (px-2.5)
- **Padding Vertical**: 6px (py-1.5)
- **Background**: #164E3F (Teal-900)
- **Border Radius**: 6px (rounded-md)
- **Display**: Flex
- **Alignment**: items-center, justify-center

**Active Number Text:**
- **Height**: 16px (h-4)
- **Padding Top**: 2px (pt-0.5)
- **Padding Bottom**: 3px (pb-[3px])
- **Font**: Urbanist, 10px (text-[10px]), Weight 500 (Medium), Line Height 10px (leading-[10px])
- **Color**: #FAFAFA (Neutral-50)

**Page Number Button (Inactive):**
- **Width**: 28px (w-7)
- **Padding Horizontal**: 10px (px-2.5)
- **Padding Vertical**: 6px (py-1.5)
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: 6px (rounded-md)
- **Display**: Flex
- **Alignment**: items-center, justify-center
- **Gap**: 2px (gap-0.5)

**Inactive Number Text:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 500 (Medium), Line Height 10px (leading-[10px])
- **Color**: #164E3F (Teal-900)

**Ellipsis (...):**
- **Width**: 28px (w-7)
- **Padding Horizontal**: 2px (px-0.5)
- **Padding Vertical**: 6px (py-1.5)
- **Background**: Transparent
- **Border Radius**: 6px (rounded-md)
- **Display**: Flex
- **Alignment**: items-center, justify-center

**Ellipsis Text:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 500 (Medium), Line Height 10px (leading-[10px])
- **Color**: #164E3F (Teal-900)
- **Content**: "..."

---

##### Pagination - Medium Size

**Container Gap:** 8px (gap-2)

**Previous/Next Button:**
- **Padding**: 8px (p-2)
- **Background**: #F4F4F5 (Zinc-100) - disabled, #F5F5F4 (Stone-100) - enabled
- **Border Radius**: 8px (rounded-lg)
- **Display**: Flex
- **Gap**: 8px (gap-2)

**Arrow Icon Container:**
- **Size**: 16px × 16px (w-4 h-4)
- **Position**: Relative

**Arrow Graphic:**
- **Size**: 8px × 5px (w-2 h-[5px])
- **Position**: Absolute
- **Previous Arrow**: left 5px, top 12.50px, rotate -90deg
- **Next Arrow**: left 6px, top 12.50px, rotate -90deg
- **Color (Disabled)**: #D6D3D1 (Stone-300)
- **Color (Enabled)**: #27272A (Zinc-800)

**Page Number Button (Active):**
- **Width**: 32px (w-8)
- **Padding Horizontal**: 12px (px-3)
- **Padding Vertical**: 8px (py-2)
- **Background**: #164E3F (Teal-900)
- **Border Radius**: 8px (rounded-lg)
- **Display**: Flex
- **Alignment**: items-center, justify-center

**Active Number Text:**
- **Padding Vertical**: 2px (py-0.5)
- **Font**: Urbanist, 12px (text-xs), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #FAFAFA (Neutral-50)

**Page Number Button (Inactive):**
- **Width**: 32px (w-8)
- **Padding Horizontal**: 12px (px-3)
- **Padding Vertical**: 8px (py-2)
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: 8px (rounded-lg)
- **Display**: Flex
- **Alignment**: items-center, justify-center
- **Gap**: 2px (gap-0.5)

**Inactive Number Text:**
- **Font**: Urbanist, 12px (text-xs), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #164E3F (Teal-900)

**Ellipsis (...):**
- **Width**: 32px (w-8)
- **Padding Horizontal**: 2px (px-0.5)
- **Padding Vertical**: 8px (py-2)
- **Background**: Transparent
- **Border Radius**: 8px (rounded-lg)
- **Display**: Flex
- **Alignment**: items-center, justify-center
- **Gap**: 2px (gap-0.5)

**Ellipsis Text:**
- **Font**: Urbanist, 12px (text-xs), Weight 600 (Semibold), Line Height 12px (leading-3)
- **Color**: #164E3F (Teal-900)
- **Content**: "..."

---

##### Size Variants

| Feature | Small | Medium | Large |
|---------|-------|--------|-------|
| Arrow Button Padding | 6px (p-1.5) | 8px (p-2) | 10px (p-2.5) |
| Arrow Button Radius | 6px (rounded-md) | 8px (rounded-lg) | 10px (rounded-[10px]) |
| Arrow Icon Size | 14px (w-3.5) | 16px (w-4) | 20px (w-5) |
| Page Button Width | 28px (w-7) | 32px (w-8) | 40px (w-10) |
| Page Button Padding | 10px/6px (px-2.5 py-1.5) | 12px/8px (px-3 py-2) | 16px/10px (px-4 py-2.5) |
| Page Button Radius | 6px (rounded-md) | 8px (rounded-lg) | 10px (rounded-[10px]) |
| Text Font Size | 10px (text-[10px]) | 12px (text-xs) | 14px (text-sm) |
| Text Weight | Medium (500) | Semibold (600) | Semibold (600) |
| Gap Between Items | 8px (gap-2) | 8px (gap-2) | 12px (gap-3) |

---

##### States

**Page Button States:**

**Active (Current Page):**
- Background: Teal-900 (#164E3F)
- Text: Neutral-50 (#FAFAFA)
- Font Weight: Medium/Semibold
- Cursor: default (not clickable)

**Inactive (Other Pages):**
- Background: Stone-100 (#F5F5F4)
- Text: Teal-900 (#164E3F)
- Font Weight: Medium/Semibold
- Cursor: pointer

**Hover (Inactive Page):**
- Background: Stone-200 (#E7E5E4)
- Text: Teal-900 (#164E3F)
- Transition: 150ms ease
- Scale: 1.05

**Pressed:**
- Background: Stone-300 (#D6D3D1)
- Scale: 0.95

**Disabled:**
- Background: Stone-50 (#FAFAF9)
- Text: Stone-400 (#A8A29E)
- Cursor: not-allowed
- Opacity: 0.5

---

**Arrow Button States:**

**Enabled:**
- Background: Stone-100 (#F5F5F4)
- Arrow: Zinc-800 (#27272A)
- Cursor: pointer

**Disabled:**
- Background: Zinc-100 (#F4F4F5)
- Arrow: Stone-300 (#D6D3D1)
- Cursor: not-allowed

**Hover (Enabled):**
- Background: Stone-200 (#E7E5E4)
- Arrow: Zinc-900 (#18181B)
- Scale: 1.05

**Pressed:**
- Background: Stone-300 (#D6D3D1)
- Scale: 0.95

---

##### Pagination Patterns

**Pattern 1: Compact (Mobile)**
```
[<] 1 2 3 ... 16 [>]
```
- Show: First 3 pages, ellipsis, last page
- Total items: 7 (2 arrows + 5 pages/ellipsis)
- Use case: Mobile, narrow screens

**Pattern 2: Standard (Desktop)**
```
[<] 1 2 3 4 5 ... 15 16 [>]
```
- Show: First 5 pages, ellipsis, last 2 pages
- Total items: 9 (2 arrows + 7 pages/ellipsis)
- Use case: Desktop, wide screens

**Pattern 3: Extended**
```
[<] 1 2 3 4 5 6 7 8 9 ... 15 16 [>]
```
- Show: First 9 pages, ellipsis, last 2 pages
- Total items: 13 (2 arrows + 11 pages/ellipsis)
- Use case: Large datasets, wide screens

**Pattern 4: Around Current**
```
[<] 1 ... 5 6 [7] 8 9 ... 16 [>]
```
- Show: First page, ellipsis, 2 before current, current, 2 after, ellipsis, last
- Dynamic based on current page
- Use case: Large page counts

**Pattern 5: Minimal**
```
Page 1 of 16  [<] [>]
```
- Text instead of page buttons
- Only prev/next arrows
- Use case: Mobile, very narrow screens

**Pattern 6: With Input**
```
[<] 1 2 3  [  7  ] / 16  [>]
```
- Direct page input field
- Total page count shown
- Use case: Quick navigation to specific page

---

##### Best Practices

**Page Display Logic:**
- Always show first and last page
- Show 2-3 pages before and after current
- Use ellipsis when gap is 2+ pages
- Limit total visible pages to 7-9 items
- Mobile: Show 3-5 pages max

**Arrow Buttons:**
- Disable "Previous" on page 1
- Disable "Next" on last page
- Use clear directional icons
- Provide tooltips: "Previous page", "Next page"

**Responsive Behavior:**
- **Desktop (1024px+)**: Show 7-9 page buttons
- **Tablet (768px)**: Show 5 page buttons
- **Mobile (320px)**: Show 3 page buttons or text-based navigation

**Performance:**
- Lazy load page content
- Pre-fetch next/previous page
- Cache recently visited pages
- Show loading state during navigation
- Maintain scroll position option

**Accessibility:**
- ARIA role: "navigation" for container
- ARIA label: "Pagination"
- ARIA current: "page" for active page
- Keyboard navigation: Tab to focus, Enter/Space to navigate, Arrow keys to move between pages
- Focus indicator clearly visible
- Screen reader: announce "[Number], page [N] of [Total]"
- Announce page changes (live region)
- Minimum touch target: 40px × 40px

**Additional Features:**
- Show total results count: "Showing 1-20 of 320 results"
- Items per page selector: "Show: [20 ▼]"
- "Go to page" input field
- "First" and "Last" buttons for large datasets
- URL updates for shareable page links
- Remember page state in session

---

##### Use Cases

**Data Tables:**
```
┌───────────────────────────────────┐
│ Name     | Email     | Status     │
│ John Doe | john@...  | Active     │
│ ...                                │
├───────────────────────────────────┤
│ Showing 1-20 of 320               │
│ [<] 1 2 [3] 4 5 ... 16 [>]       │
└───────────────────────────────────┘
```

**Search Results:**
```
┌───────────────────────────────────┐
│ Results for "design system" (320) │
│                                   │
│ [Result 1]                        │
│ [Result 2]                        │
│ ...                               │
│                                   │
│ Page [<] 1 2 [3] 4 5 ... 16 [>]  │
└───────────────────────────────────┘
```

**Product Listings:**
```
┌──────────────────────────────────┐
│ [Product] [Product] [Product]    │
│ [Product] [Product] [Product]    │
│ [Product] [Product] [Product]    │
│                                  │
│     [<] 1 2 [3] 4 ... 10 [>]    │
└──────────────────────────────────┘
```

**Blog Posts:**
```
┌──────────────────────────────────┐
│ [Post Title]                     │
│ Excerpt text...                  │
│                                  │
│ [Post Title]                     │
│ Excerpt text...                  │
│                                  │
│ [<] Newer | Page 3 of 12 | Older [>] │
└──────────────────────────────────┘
```

---

##### With Additional Controls

**Full Pagination Bar:**
```
┌────────────────────────────────────────────────┐
│ Showing 1-20 of 320 | Items per page: [20 ▼]  │
│ [First] [<] 1 2 [3] 4 5 ... 16 [>] [Last]     │
│ Go to page: [___] [Go]                         │
└────────────────────────────────────────────────┘
```

**Compact with Info:**
```
┌────────────────────────────────────┐
│ 1-20 of 320  [<] Page 3 [>] [20▼] │
└────────────────────────────────────┘
```

---

#### Header / Top Navigation Bar

**Header Container:**
- **Width**: 1232px (w-[1232px]) - full width example
- **Height**: Auto (based on content)
- **Padding**: 20px from edges
- **Layout**: Flex row, space between (justify-between items-center)
- **Background**: Usually #FFFFFF (White) or transparent
- **Border Bottom**: 1px solid #F2F3F4 (optional, for separation)

---

#### Header Elements

**Page Title (Large):**
- **Font**: Urbanist, 20px (text-xl), Weight 700 (Bold), Line Height 28px (leading-7)
- **Color**: #164E3F (Teal-900)
- **Use case**: Main page heading

**Page Title (Medium):**
- **Font**: Urbanist, 20px (text-xl), Weight 700 (Bold), Line Height 24px (leading-6)
- **Color**: #164E3F (Teal-900)
- **Use case**: Section heading

**Back Button:**
- **Size**: Medium icon button
- **Padding**: 8px (p-2)
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: 8px (rounded-lg)
- **Gap**: 8px (gap-2)
- **Icon**:
  - Size: 16px (w-4 h-4)
  - Color: #164E3F (Teal-900)
  - Transform: rotate(90deg) for left arrow (origin-top-left)
- **Layout**: Positioned before page title with gap 10px (gap-2.5)
- **States**:
  - Hover: Background #E7E5E4 (Stone-200)
  - Active: Background #D6D3D1 (Stone-300)

**Breadcrumb (Header):**
- **Layout**: Flex row, items-center, Gap 4px (gap-1)
- **Font**: Urbanist, 20px (text-xl), Weight 700 (Bold) for active, Weight 500 (Medium) for inactive, Line Height 24px (leading-6)
- **Current Page**: Color #164E3F (Teal-900)
- **Separator**: "/" (forward slash), Color #737373 (Neutral-500), Weight 500
- **Parent Pages**: Color #737373 (Neutral-500), Weight 500
- **Chevron Icon**:
  - Size: 16px (w-4 h-4)
  - Color: #737373 (Neutral-500)
  - Position: After last breadcrumb item
- **Example**: "Dashboard / Page >"

**Search Input (Header - Large):**
- **Width**: 288px (w-72)
- **Padding**: 10px 16px (px-4 py-2.5)
- **Background**: #F4F4F5 (Zinc-100)
- **Border**: 1px solid #F4F4F5 (Zinc-100)
- **Outline**: 1px, offset -1px (outline-offset-[-1px])
- **Border Radius**: 20px (rounded-[20px])
- **Gap**: 6px (gap-1.5)
- **Placeholder**:
  - Font: Urbanist, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
  - Color: #737373 (Neutral-500)
  - Example: "Search placeholder"
- **Icon**:
  - Size: 16px (w-4 h-4), actual icon 14px (w-3.5 h-3.5)
  - Color: #164E3F (Teal-900)
  - Position: Right side
- **States**:
  - Focus: Border color #164E3F, Shadow 0 0 0 3px rgba(22, 78, 63, 0.1)
  - Filled: Show clear icon

**Icon Button (Header - Large Secondary):**
- **Size**: 40px × 40px (overall with padding)
- **Padding**: 10px (p-2.5)
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: 20px (rounded-[20px])
- **Gap**: 8px (gap-2)
- **Icon**:
  - Size: 16px (w-4 h-4), actual icon ~14px (w-3.5 h-3.5)
  - Color: #164E3F (Teal-900)
- **States**:
  - Hover: Background #E7E5E4 (Stone-200)
  - Active: Background #D6D3D1 (Stone-300)
- **Use case**: Settings, notifications, help icons

**Icon Button with Badge:**
- **Base**: Same as Icon Button Large Secondary
- **Badge**:
  - Size: 14px × 14px (w-3.5 h-3.5) container
  - Padding: 2px (p-0.5)
  - Position: Absolute, left 18px, top 6px (relative to button)
  - Background: None (transparent container)
- **Dot**:
  - Size: 8px × 8px (w-2 h-2)
  - Padding horizontal: 2px (px-0.5)
  - Background: #EF4444 (Red-500)
  - Border Radius: 10px (rounded-[10px])
  - Position: Centered in badge container
- **Gap**: 10px (gap-2.5) for multiple badges
- **Use case**: Notification indicator, unread messages

**User Profile Section:**
- **Width**: 176px (w-44)
- **Layout**: Flex row, items-center, justify-end, Gap 14px (gap-3.5)
- **User Name**:
  - Font: Urbanist, 16px (text-base), Weight 700 (Bold), Line Height 20px (leading-5)
  - Color: #164E3F (Teal-900)
  - Alignment: Right (items-end)
  - Gap: 2px (gap-0.5) in container
  - Example: "Andrew Forbist"
- **Avatar**:
  - Size: 36px × 36px (w-9 h-9)
  - Border Radius: 56px (rounded-[56px]) for outer container, 32px (rounded-[32px]) for inner
  - Background: #ECFCCB (Lime-200) or image
  - Overflow: Hidden
  - Border Radius inner: 24px (rounded-3xl)
- **Interactive**: Clickable for dropdown menu
- **States**:
  - Hover: Slight shadow or scale
  - Active: Show dropdown with user menu

**User Profile Section (Compact):**
- **Layout**: Avatar only, no name
- **Avatar**: Same 36px size
- **Use case**: Mobile or compact headers

---

#### Header Layout Patterns

**Pattern 1: Title + Search + Icons + User**
```
┌──────────────────────────────────────────────────────┐
│ Dashboard         [Search] [Icon] [Icon] Name Avatar │
└──────────────────────────────────────────────────────┘
```
- **Left**: Page title (Teal-900, 20px Bold)
- **Right**: Search (288px) + Icon buttons (gap-2.5) + User profile (176px)
- **Total spacing**: gap-5 (20px) between sections

**Pattern 2: Back + Title + Icons + User**
```
┌──────────────────────────────────────────────────────┐
│ [<] Dashboard     [Search] [Icon] [Icon] Name Avatar │
└──────────────────────────────────────────────────────┘
```
- **Left**: Back button (Medium) + Page title (gap-2.5)
- **Right**: Search + Icon buttons + User profile
- **Use case**: Sub-pages with navigation

**Pattern 3: Title + Icons + Avatar (Compact)**
```
┌─────────────────────────────────────┐
│ Dashboard   [Icon] [Icon] [Icon] 👤 │
└─────────────────────────────────────┘
```
- **Left**: Page title only
- **Right**: Icon buttons (gap-2.5) + Avatar only (no name)
- **Use case**: Medium-sized screens

**Pattern 4: Breadcrumb + Icons + Avatar**
```
┌─────────────────────────────────────────────┐
│ Dashboard / Page >   [Icon] [Icon] [Icon] 👤 │
└─────────────────────────────────────────────┘
```
- **Left**: Breadcrumb navigation with chevron
- **Right**: Icon buttons + Avatar
- **Use case**: Multi-level navigation

**Pattern 5: Back + Title + Icons + Avatar (Compact)**
```
┌──────────────────────────────────────┐
│ [<] Dashboard   [Icon] [Icon] [Icon] 👤 │
└──────────────────────────────────────┘
```
- **Left**: Back button + Title (gap-2.5)
- **Right**: Icon buttons + Avatar only
- **Use case**: Compact sub-pages

---

#### Header Spacing & Alignment

**Container Spacing:**
- **Horizontal padding**: 20px from edges (left-[20px])
- **Vertical padding**: 20px top (top-[20px])
- **Between elements**: Space between (justify-between)
- **Vertical spacing between rows**: 58px (78-20, 136-78, etc.)

**Section Spacing:**
- **Title to actions**: Space between (flex)
- **Between icon buttons**: 10px (gap-2.5)
- **Search to icons**: 20px (gap-5)
- **Icons to user profile**: 20px (gap-5) or 10px (gap-2.5)
- **Back button to title**: 10px (gap-2.5)
- **Name to avatar**: 14px (gap-3.5)

**Alignment:**
- **Default**: items-center (vertical center)
- **User name**: items-end (right-aligned text)
- **Avatar**: Center in container

---

#### Header States & Interactions

**Search States:**
- **Default**: Zinc-100 background
- **Focus**: Teal-900 border, shadow
- **Filled**: Show clear button (X icon)
- **Disabled**: Opacity 0.5

**Icon Button States:**
- **Default**: Stone-100 background
- **Hover**: Stone-200 background
- **Active**: Stone-300 background
- **With Badge**: Red dot indicator
- **Disabled**: Opacity 0.5

**User Profile States:**
- **Default**: Normal display
- **Hover**: Slight shadow, cursor pointer
- **Active/Clicked**: Show dropdown menu
- **Dropdown Menu**:
  - Background: #FFFFFF
  - Border Radius: 8px
  - Shadow: var(--shadow-lg)
  - Padding: 8px
  - Min Width: 200px
  - Items: Profile, Settings, Logout

**Back Button States:**
- **Default**: Stone-100 background
- **Hover**: Stone-200 background
- **Active**: Stone-300 background
- **Disabled**: Opacity 0.5, cursor not-allowed

---

#### Header Best Practices

**Typography:**
- **Page Title**: Urbanist, 20px, Weight 700, Line Height 24-28px
- **Breadcrumb**: Urbanist, 20px, Weight 500-700, Line Height 24px
- **User Name**: Urbanist, 16px, Weight 700, Line Height 20px
- **Search Placeholder**: Urbanist, 12px, Weight 400, Line Height 16px

**Spacing:**
- Maintain 20px padding from edges
- Use 10px gaps between related elements
- Use 20px gaps between major sections
- Keep consistent vertical alignment

**Accessibility:**
- Use semantic HTML (header, nav tags)
- Include ARIA labels for icon-only buttons
- Keyboard navigation support (Tab, Enter, Escape)
- Focus indicators on all interactive elements
- Screen reader announcements for notifications
- Ensure 44px minimum touch target size

**Responsive Behavior:**
- **Desktop (1024px+)**: Full layout with search and user name
- **Tablet (768px)**: Hide user name, keep avatar
- **Mobile (320px)**:
  - Hamburger menu for icon buttons
  - Avatar only
  - Search in toolbar or expandable
  - Page title may truncate

**Performance:**
- Sticky header option: position sticky, top 0
- Z-index: 100 to stay above content
- Shadow on scroll: Add shadow when page scrolls
- Debounce search input

**Common Use Cases:**
- **Admin Dashboard**: Title, search, notification icon, settings, user profile
- **Application**: Back button, breadcrumb, action icons, user avatar
- **E-commerce**: Logo/title, search, cart icon, wishlist, account
- **CMS**: Back, title, save/publish buttons, preview, user
- **Mobile App**: Back, title, share icon, more menu, avatar

---

#### Footer

**Footer Container:**
- **Width**: 1232px (w-[1232px]) - full width example
- **Padding**: 20px (p-5)
- **Gap**: 20px (gap-5) between rows
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Overflow**: Hidden
- **Background**: Usually #FFFFFF (White) or #F7F8F8 (Gray-BG Subtle)

---

#### Footer Elements

**Copyright Text:**
- **Font**: Urbanist, 12px (text-xs), Weight 500 (Medium), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Example**: "Copyright © 2024 Peterdraw"
- **Alignment**: Left (horizontal layout) or Center (vertical layout)

**Footer Links:**
- **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal), Line Height 16px (leading-4)
- **Color**: #D6D3D1 (Stone-300)
- **Gap**: 16px (gap-4) between links
- **Examples**: "Privacy Policy", "Term and conditions", "Contact"
- **States**:
  - Hover: Color #164E3F (Teal-900), Underline
  - Active: Color #0F3D30 (Darker Teal)
  - Visited: Same as default

**Social Media Icons:**
- **Size**: 24px × 24px (w-6 h-6) container
- **Icon Color**: #D6D3D1 (Stone-300)
- **Gap**: 12px (gap-3) between icons
- **Common Icons**:
  - LinkedIn: 20px × 20px actual icon (w-5 h-5)
  - Twitter/X: Multiple paths
  - Instagram: Circle + camera shapes
  - YouTube: Play button shape
  - Facebook: 'f' shape
- **States**:
  - Hover: Color #164E3F (Teal-900), Scale 1.1
  - Active: Color #0F3D30
- **Interactive**: Links to social profiles

---

#### Footer Layout Patterns

**Pattern 1: Horizontal Footer (Desktop)**
```
┌────────────────────────────────────────────────────────┐
│ Copyright © 2024  Privacy | Terms | Contact  [Icons]   │
└────────────────────────────────────────────────────────┘
```
- **Container Height**: 24px (h-6) content area
- **Layout**: Flex row, justify-between, items-center
- **Left Section**:
  - Copyright text
  - Footer links (gap-4)
  - Total gap between copyright and links: 20px (gap-5)
- **Right Section**:
  - Social media icons (gap-3)
- **Use case**: Desktop, wide screens

**Pattern 2: Vertical Footer (Mobile/Centered)**
```
┌──────────────────────┐
│  Copyright © 2024    │
│ Privacy | Terms | ... │
│     [Icon Icons]     │
└──────────────────────┘
```
- **Width**: 384px (w-96) max
- **Layout**: Flex column, items-center, gap-2.5 (10px)
- **Row 1**: Copyright text (centered)
- **Row 2**: Footer links (centered, gap-4)
- **Row 3**: Social media icons (centered, gap-3)
- **Use case**: Mobile, tablet, narrow screens

---

#### Footer Spacing & Alignment

**Horizontal Layout (Desktop):**
- **Padding**: 20px all sides (p-5)
- **Gap between sections**: Space between (justify-between)
- **Copyright to links**: 20px (gap-5)
- **Between links**: 16px (gap-4)
- **Between icons**: 12px (gap-3)
- **Height**: Auto, minimum 24px content

**Vertical Layout (Mobile):**
- **Padding**: 20px all sides (p-5)
- **Gap between rows**: 10px (gap-2.5)
- **Between links**: 16px (gap-4)
- **Between icons**: 12px (gap-3)
- **Alignment**: All centered (items-center)
- **Width**: Max 384px (w-96)

**Container Alignment:**
- **Horizontal**: items-center (vertical center)
- **Vertical**: items-center (horizontal center)

---

#### Footer States & Interactions

**Link States:**
- **Default**: Stone-300 (#D6D3D1)
- **Hover**: Teal-900 (#164E3F), underline, transition 200ms
- **Active**: Darker Teal (#0F3D30)
- **Focus**: Teal-900, focus ring
- **Visited**: Same as default (no color change)

**Icon States:**
- **Default**: Stone-300 (#D6D3D1)
- **Hover**: Teal-900 (#164E3F), scale 1.1, transition 200ms
- **Active**: Darker Teal (#0F3D30), scale 1.05
- **Focus**: Teal-900, focus ring

**Copyright Text:**
- **Static**: No interactive states
- **Selectable**: Text can be selected/copied

---

#### Footer Best Practices

**Typography:**
- **Copyright**: Urbanist, 12px, Weight 500, Line Height 16px
- **Links**: Urbanist, 12px, Weight 400, Line Height 16px
- **Consistent**: Use same font family as rest of site

**Spacing:**
- Maintain 20px padding from edges
- Use 16px gaps between footer links
- Use 12px gaps between social icons
- Keep vertical spacing at 10px for stacked layout

**Accessibility:**
- Use semantic HTML (footer tag)
- Include ARIA labels for social media icons (e.g., "Visit us on LinkedIn")
- Keyboard navigation support (Tab, Enter)
- Focus indicators on all links and icons
- Sufficient color contrast (Stone-300 on white may need darker shade for WCAG AA)
- Screen reader friendly link text (avoid "Click here")

**Responsive Behavior:**
- **Desktop (1024px+)**: Horizontal layout (Pattern 1)
- **Tablet (768px)**: May switch to vertical or keep horizontal with wrapping
- **Mobile (320px-767px)**: Vertical centered layout (Pattern 2)
- **Breakpoint**: 768px to switch between layouts
- Consider stacking on smaller screens

**Content Guidelines:**
- **Copyright**: Always include current year, update annually
- **Required Links**: Privacy Policy, Terms of Service/Conditions
- **Optional Links**: Contact, About, Cookies Policy, Accessibility Statement
- **Social Icons**: Only include active social profiles
- **Order**: Most important links first (Privacy, Terms usually required by law)

**SEO & Legal:**
- Privacy Policy and Terms links required for GDPR/legal compliance
- Include company/author name in copyright
- Make links actual anchor tags, not just styled text
- Social icons should have proper rel="noopener" for external links

**Color Considerations:**
- Stone-300 (#D6D3D1) has low contrast on white background
- Consider using Stone-400 or Stone-500 for better accessibility
- Or use Neutral-500 (#737373) for links to meet WCAG AA (4.5:1 ratio)
- Hover state should always be accessible color (Teal-900 works well)

---

#### Footer Variants

**Minimal Footer:**
```
Copyright © 2024 Company Name
```
- Just copyright text, centered
- No links, no icons
- Use case: Landing pages, simple sites

**Footer with Multiple Link Columns:**
```
┌─────────────────────────────────────────────┐
│ [Products]  [Company]  [Resources]  [Icons] │
│   Link        Link       Link                │
│   Link        Link       Link                │
└─────────────────────────────────────────────┘
```
- Multiple column layout
- Copyright at bottom or separate row
- Use case: Large sites, corporate websites

**Footer with Newsletter:**
```
┌──────────────────────────────────────────────┐
│ Subscribe:  [Email Input] [Subscribe Button] │
│ Copyright © 2024 | Privacy | Terms  [Icons]  │
└──────────────────────────────────────────────┘
```
- Newsletter signup in footer
- Links and icons below
- Use case: Marketing sites, blogs

---

#### Tab Pills / Pill Navigation

Компактные кнопки-таблетки для переключения между разделами или фильтрами.

**Container:**
- **Padding**: 20px (p-5)
- **Display**: Inline-flex
- **Alignment**: items-start, justify-start
- **Gap**: 20px (gap-5) between pills
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Overflow**: Hidden

**Pill Button (Active):**
- **Padding Horizontal**: 16px (px-4)
- **Padding Vertical**: 6px (py-1.5)
- **Background**: #164E3F (Teal-900)
- **Border Radius**: 16px (rounded-2xl) - pill shape
- **Display**: Flex
- **Alignment**: items-center, justify-center
- **Gap**: 4px (gap-1)

**Text (Active):**
- **Font**: Urbanist, 12px (text-xs), Weight 600 (Semibold), Line Height 16px (leading-4)
- **Color**: #FAFAFA (Neutral-50)
- **Alignment**: justify-start

**Pill Button (Inactive):**
- **Padding Horizontal**: 16px (px-4)
- **Padding Vertical**: 6px (py-1.5)
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: 16px (rounded-2xl)
- **Display**: Flex
- **Alignment**: items-center, justify-center
- **Gap**: 4px (gap-1)

**Text (Inactive):**
- **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Alignment**: justify-start

---

**Spacing Breakdown:**
- **Padding horizontal**: 16px inside each pill
- **Padding vertical**: 6px inside each pill
- **Gap between pills**: 20px
- **Border radius**: 16px для pill shape

**States:**

**Active:**
- Background: Teal-900 (#164E3F)
- Text: Neutral-50 (#FAFAFA)
- Font Weight: 600 (Semibold)
- Cursor: default (not clickable when active)

**Inactive (Default):**
- Background: Stone-100 (#F5F5F4)
- Text: Zinc-800 (#27272A)
- Font Weight: 400 (Normal)
- Cursor: pointer

**Hover (Inactive):**
- Background: Stone-200 (#E7E5E4)
- Text: Zinc-900 (#18181B)
- Transition: 150ms ease
- Scale: 1.02

**Pressed (Inactive):**
- Background: Stone-300 (#D6D3D1)
- Scale: 0.98

**Disabled:**
- Background: Stone-50 (#FAFAF9)
- Text: Stone-400 (#A8A29E)
- Opacity: 0.6
- Cursor: not-allowed

**Focus:**
- Outline: 2px solid Teal-900
- Outline offset: 2px

---

**Size Variants:**

**Small:**
- Padding: 12px 8px (px-3 py-2)
- Font: 10px (text-[10px])
- Border radius: 12px (rounded-xl)
- Height: ~28px

**Medium (Default):**
- Padding: 16px 6px (px-4 py-1.5)
- Font: 12px (text-xs)
- Border radius: 16px (rounded-2xl)
- Height: ~28px

**Large:**
- Padding: 20px 8px (px-5 py-2)
- Font: 14px (text-sm)
- Border radius: 20px (rounded-[20px])
- Height: ~36px

---

**Color Variants:**

**Primary (Teal):**
- Active: Teal-900 background, Neutral-50 text
- Inactive: Stone-100 background, Zinc-800 text

**Secondary (Blue):**
- Active: Blue-500 (#3B82F6) background, White text
- Inactive: Blue-50 (#EFF6FF) background, Blue-700 text

**Success (Green):**
- Active: Emerald-600 (#059669) background, White text
- Inactive: Emerald-50 (#ECFDF5) background, Emerald-700 text

**Minimal (Ghost):**
- Active: Transparent background, Teal-900 text, 1px border Teal-900
- Inactive: Transparent background, Zinc-600 text

---

**With Icons:**

**Icon Left:**
- Icon size: 16px (w-4 h-4)
- Position: Before text
- Gap: 4px (gap-1)
- Icon color: Matches text color

**Icon Right:**
- Icon size: 16px (w-4 h-4)
- Position: After text
- Gap: 4px (gap-1)
- Use case: Dropdown indicator, close button

**Icon Only:**
- Padding: 8px (p-2) - square padding
- Icon: 16px (w-4 h-4)
- No text
- Border radius: rounded-2xl
- Use case: Compact filters

---

**With Badge/Count:**

Add notification count
- **Badge**: Small circle or pill
- **Position**: Top-right corner or after text
- **Size**: 16px × 16px or auto width
- **Background**: Red-500 (notifications) or Teal-900 (count)
- **Text**: 10px White
- **Example**: "All (5)", "Active (12)"

---

**Use Cases:**
- Tab navigation (All, Active, Completed, Archived)
- Category filters (All Categories, Design, Development, Marketing)
- Status filters (All, Pending, Approved, Rejected)
- View switchers (List, Grid, Calendar)
- Time range selectors (Day, Week, Month, Year)
- Sort options (Recent, Popular, Trending)
- Type filters (All, Images, Videos, Documents)

**Best Practices:**
- Keep labels concise (1-2 words, max 15 characters)
- Provide clear active state indication
- Use consistent pill sizes in a group
- Limit to 3-7 options per row
- Wrap to multiple rows if needed
- Make entire pill clickable
- Provide keyboard navigation (Arrow keys to switch)
- Announce active state to screen readers

**Accessibility:**
- ARIA role: "tablist" for container, "tab" for each pill
- ARIA selected: "true" for active pill
- Keyboard navigation: Tab to focus, Arrow keys to navigate, Enter/Space to select
- Focus indicator: Visible outline on focused pill
- Screen reader: Announce "[Label], tab, [selected/not selected]"
- High contrast mode: Ensure borders visible
- Minimum touch target: 44px × 44px (especially on mobile)

**Layout Patterns:**

**Horizontal Row:**
```
[All] [Active] [Completed] [Archived]
```
- Display: flex row
- Gap: 8px-20px (gap-2 to gap-5)
- Wrap: flex-wrap on small screens

**Horizontal Scroll (Mobile):**
```
[All] [Active] [Completed] →
```
- Overflow-x: auto
- Snap scroll: optional
- Hide scrollbar: optional

**Vertical Stack:**
```
[All]
[Active]
[Completed]
```
- Display: flex-col
- Gap: 8px (gap-2)
- Use case: Sidebar filters

**Grid Layout:**
```
[All]        [Active]
[Completed]  [Archived]
```
- Grid: 2 columns (grid-cols-2)
- Gap: 12px (gap-3)
- Use case: Category filters

**Segmented Control:**
```
┌──────┬────────┬──────────┐
│  All │ Active │ Archived │
└──────┴────────┴──────────┘
```
- Connected pills, no gap
- Border between items
- Equal width segments
- Use case: View switcher

**With Divider:**
```
[All] [Active] | [Settings] [Help]
```
- Separate groups with vertical divider
- Divider: 1px Stone-300, 16px height

---

#### Chat / Messaging

**Chat Container:**
- **Width**: 516px (w-[516px]) example container
- **Padding**: 20px (p-5)
- **Gap**: 16px (gap-4) between messages
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Overflow**: Hidden
- **Background**: Usually #FFFFFF (White) or #F7F8F8 (Gray-BG Subtle)
- **Layout**: Flex column (flex-col)

---

#### Message Bubble Elements

**Message Container (Outgoing - Right):**
- **Width**: 460px (w-[460px]) max container
- **Padding Vertical**: 4px (py-1)
- **Layout**: Flex row, justify-end, items-end
- **Gap**: 12px (gap-3)
- **No Avatar**: Outgoing messages typically don't show sender avatar
- **Use case**: Messages sent by current user

**Message Container (Incoming - Left):**
- **Width**: 460px (w-[460px]) max container
- **Padding Vertical**: 4px (py-1)
- **Layout**: Flex row, justify-start, items-start
- **Gap**: 12px (gap-3)
- **Avatar**: 36px × 36px (w-9 h-9), Lime-200 background
- **Use case**: Messages received from other users

---

#### Message Header

**Message Meta (Outgoing):**
- **Layout**: Flex row, items-center, Gap 6px (gap-1.5)
- **Alignment**: Right (justify-start within right-aligned container)
- **Elements**:
  - Name: Lato, 12px (text-xs), Weight 400, Line Height 12px (leading-3), Color #52525B (Zinc-600)
  - Dot Separator: 4px × 4px (w-1 h-1), Background #E7E5E4 (Stone-200), Border Radius full
  - Timestamp: Lato, 12px (text-xs), Weight 400, Line Height 12px (leading-3), Color #52525B (Zinc-600)
  - Chevron Icon (optional): 16px (w-4 h-4), Color #171717 (Neutral-900)
- **Example**: "Name • 9.46 PM >"

**Message Meta (Incoming):**
- **Layout**: Flex row, items-center, Gap 6px (gap-1.5)
- **Alignment**: Left (justify-start)
- **Height**: 16px (h-4)
- **Elements**: Same as outgoing but without chevron icon
- **Example**: "Name • 9.46 PM"

---

#### Message Bubble

**Text Bubble (Outgoing):**
- **Max Width**: 384px (max-w-96)
- **Padding**: 12px 16px 14px (px-4 pt-3 pb-3.5)
- **Background**: #D1FAE5 (Emerald-100)
- **Border Radius**: rounded-tl-xl rounded-bl-xl rounded-br-xl (12px)
  - Top-left: 12px
  - Bottom-left: 12px
  - Bottom-right: 12px
  - Top-right: 0 (square corner, pointing right)
- **Text**:
  - Font: Lato, 12px (text-xs), Weight 400, Line Height 20px (leading-5)
  - Color: #171717 (Neutral-900)
- **Gap**: 10px (gap-2.5) internal
- **Alignment**: Right side of chat
- **Use case**: User's own messages

**Text Bubble (Incoming):**
- **Max Width**: 384px (max-w-96)
- **Padding**: 12px 16px 14px (px-4 pt-3 pb-3.5)
- **Background**: #FECACA (Rose-200)
- **Border Radius**: rounded-tr-xl rounded-bl-xl rounded-br-xl (12px)
  - Top-right: 12px
  - Bottom-left: 12px
  - Bottom-right: 12px
  - Top-left: 0 (square corner, pointing left)
- **Text**: Same as outgoing
- **Alignment**: Left side of chat
- **Use case**: Messages from other users

---

#### Message Attachments

**Image Attachment (Incoming):**
- **Max Width**: 480px (max-w-[480px])
- **Padding**: 8px (p-2)
- **Background**: #FECACA (Rose-200) - matches message bubble color
- **Border Radius**: rounded-tr-md rounded-bl-md rounded-br-md (6px)
  - Top-right: 6px
  - Bottom-left: 6px
  - Bottom-right: 6px
  - Top-left: 0 (square corner)
- **Image Container**:
  - Size: 144px × 144px (w-36 h-36)
  - Background: #E5E5E5 (Neutral-200) placeholder
  - Border Radius: Same as outer container (rounded-tr-md rounded-bl-md rounded-br-md)
  - Overflow: Hidden
  - Object-fit: Cover (for actual images)
- **Gap**: 10px (gap-2.5) internal
- **Use case**: Image attachments in chat

**Image Attachment (Outgoing):**
- Same structure but:
  - Background: #D1FAE5 (Emerald-100)
  - Border Radius: rounded-tl-md rounded-bl-md rounded-br-md (mirror of incoming)

---

#### Avatar

**Chat Avatar:**
- **Size**: 36px × 36px (w-9 h-9)
- **Border Radius**: 20px (rounded-[20px]) outer, 32px (rounded-[32px]) inner, 40px (rounded-[40px]) for photo container
- **Background**: #ECFCCB (Lime-200) or profile image
- **Overflow**: Hidden
- **Position**: Top-left of incoming message container
- **Use case**: Sender identification

---

#### Message Spacing & Alignment

**Message Bubble Spacing:**
- **Gap between header and bubble**: 8px (gap-2)
- **Gap between bubbles (same sender)**: 4px
- **Gap between messages (different sender)**: 16px (gap-4)
- **Max bubble width**: 384px for text, 480px for attachments
- **Padding inside bubble**: 12px-16px

**Message Container Alignment:**
- **Outgoing**: justify-end, items-end (right-aligned)
- **Incoming**: justify-start, items-start (left-aligned)
- **Avatar gap**: 12px (gap-3) from message content

**Chat Container Spacing:**
- **Padding**: 20px (p-5) from edges
- **Gap between message groups**: 16px (gap-4)

---

#### Message States & Interactions

**Text Bubble States:**
- **Default**: Emerald-100 (outgoing) or Rose-200 (incoming)
- **Hover**: Slight shadow or opacity change (0.9)
- **Selected**: Border 2px solid Teal-900
- **Sending**: Opacity 0.7, loading indicator
- **Failed**: Border 2px solid Red-500, retry icon

**Image Attachment States:**
- **Loading**: Skeleton loader or spinner
- **Loaded**: Full image displayed
- **Error**: Placeholder with error icon
- **Hover**: Cursor pointer, slight scale (1.02)
- **Click**: Open lightbox/full view

**Message Actions:**
- **Chevron Icon**: Shows on hover, reveals message menu
- **Menu Options**: Edit, Delete, React, Reply, Forward
- **Long Press (mobile)**: Shows action menu
- **Swipe (mobile)**: Reply gesture

---

#### Chat Best Practices

**Typography:**
- **Sender Name**: Lato, 12px, Weight 400, Line Height 12px
- **Timestamp**: Lato, 12px, Weight 400, Line Height 12px
- **Message Text**: Lato, 12px, Weight 400, Line Height 20px
- **Consistent**: Use Lato for all chat text

**Color Coding:**
- **Outgoing**: Emerald-100 (#D1FAE5) - green tint for user's messages
- **Incoming**: Rose-200 (#FECACA) - pink/red tint for received messages
- **Alternative**: Use same color (e.g., Blue-Subtle) for both, differentiate by alignment only
- **System Messages**: Neutral-100 background, centered

**Spacing:**
- Maintain consistent padding inside bubbles (12-16px)
- Keep readable max-width (384px for text)
- Use adequate line-height (20px) for readability
- Group messages from same sender with minimal gap (4px)
- Separate different senders with larger gap (16px)

**Accessibility:**
- Use semantic HTML (article for messages, time tag for timestamps)
- Include ARIA labels for sender, timestamp, message status
- Keyboard navigation support (arrow keys to navigate messages)
- Focus indicators on interactive elements
- Screen reader announcements for new messages
- High contrast mode support
- Alt text for image attachments

**Responsive Behavior:**
- **Desktop (1024px+)**: Full width bubbles up to max-width
- **Tablet (768px)**: Slightly reduced max-width
- **Mobile (320px)**:
  - Reduce max bubble width to fit screen
  - Stack longer messages vertically
  - Touch-friendly targets (minimum 44px)
  - Swipe gestures for actions

**Performance:**
- Virtualize message list for long conversations
- Lazy load images and attachments
- Paginate old messages (load on scroll up)
- Optimize avatar images (use thumbnails)
- Debounce typing indicators

**Message Features:**
- **Typing Indicator**: Animated dots when other user is typing
- **Read Receipts**: Checkmarks (single/double) for sent/read status
- **Reactions**: Emoji reactions below message bubble
- **Replies**: Quoted message above new message
- **Timestamps**: Group by date with dividers (Today, Yesterday, date)
- **Delivery Status**: Sending, Sent, Delivered, Read

**Common Use Cases:**
- **Customer Support**: Live chat with agents
- **Team Communication**: Internal messaging (Slack-style)
- **Social Messaging**: Personal conversations (WhatsApp-style)
- **In-App Chat**: Feature within larger application
- **Comments/Discussions**: Threaded conversations

**Message Types:**
- **Text**: Plain text messages
- **Images**: Photo attachments
- **Files**: Document attachments with file info
- **Links**: URL previews with metadata
- **Voice**: Audio message with playback controls
- **Video**: Video attachments or inline player
- **System**: Automated messages (User joined, Settings changed)

---

#### Chat Variants

**Group Chat:**
```
[Avatar] Name • Time
         Message bubble with longer text...

[Avatar] Different Name • Time
         Another message here
```
- Show avatars for all participants
- Display sender name for each message
- Color-code by sender or use same color

**One-on-One Chat:**
```
         My message (right, no avatar)  •

• Other's message (left, with avatar)
```
- Hide avatar for own messages
- Show avatar only for received messages
- Clear visual separation

**Chat with Reactions:**
```
         Message bubble
         👍 ❤️ 😂  (below bubble)
```
- Emoji reactions below bubble
- Show count if multiple reactions
- Hover to see who reacted

**Chat with Replies:**
```
         ┌─ Original message preview
         └─ Reply text here
```
- Show quoted/replied message above
- Indent or connect with line
- Tap to scroll to original

---

#### Chat List / Inbox

**Chat List Container:**
- **Width**: 384px (w-96)
- **Padding**: 16px (p-4)
- **Background**: #F5F5F5 (Neutral-100)
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Gap**: 16px (gap-4) between chat items
- **Layout**: Flex column (flex-col)
- **Overflow**: Hidden or scroll

---

#### Chat List Item

**List Item Container:**
- **Padding**: 8px 16px (px-2 py-4)
- **Gap**: 16px (gap-4) between avatar and content
- **Layout**: Flex row, items-center
- **Background**: Transparent (default)
- **Border Radius**: 12px (rounded-xl) for active state
- **Outline**: 1px solid #86EFAC (Green-300) for active/selected state
- **Offset**: -1px (outline-offset-[-1px])

**States:**
- **Default**: Transparent background, no outline
- **Hover**: Background #FAFAFA (Neutral-50) or #E5E5E5 (Neutral-200)
- **Active/Selected**: Background #F5F5F5 (Neutral-100), Outline 1px solid #86EFAC (Green-300)
- **Pressed**: Background #E5E5E5 (Neutral-200)

---

#### Chat List Elements

**Avatar:**
- **Size**: 36px × 36px (w-9 h-9)
- **Outer Background**: #FECACA (Rose-200) - placeholder or status indicator
- **Border Radius**: 20px (rounded-[20px]) outer, 32px (rounded-[32px]) middle, 40px (rounded-[40px]) inner
- **Inner Background**: #ECFCCB (Lime-200) or user photo
- **Overflow**: Hidden
- **Use case**: User profile picture with optional status ring

**Content Container:**
- **Flex**: 1 (flex-1)
- **Height**: 44px (h-11)
- **Padding Top**: 1px (pt-px)
- **Layout**: Flex column, justify-center, items-start
- **Gap**: 4px (gap-1) between rows

---

#### First Row (Name + Badge + Time)

**Layout:**
- **Display**: Flex row, items-baseline (or items-center)
- **Gap**: 8px (gap-2)
- **Full Width**: self-stretch

**User Name:**
- **Flex**: 1 in container with gap-1.5
- **Font**: Lato, 14px (text-sm), Weight 600 (Semibold), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Example**: "Helen Martinez"

**Role/Status Badge:**
- **Padding**: 8px 2px (px-2 py-0.5)
- **Background**: #D1FAE5 (Emerald-100)
- **Border Radius**: 12px (rounded-xl)
- **Gap**: 10px (gap-2.5) internal
- **Text**:
  - Font: Lato, 12px (text-xs), Weight 400, Line Height 12px (leading-3)
  - Color: #52525B (Zinc-600)
  - Line Clamp: 1 (line-clamp-1)
  - Example: "Trainer", "Admin", "Customer"
- **Use case**: Role indicator, user type, or status label

**Timestamp:**
- **Font**: Lato, 12px (text-xs), Weight 400, Line Height 12px (leading-3)
- **Color**:
  - Default/With Unread: #171717 (Neutral-900)
  - Active/Selected: #52525B (Zinc-600)
- **Example**: "09:15 AM"
- **Format**: 12-hour time with AM/PM

---

#### Second Row (Message Preview + Unread Badge)

**Layout:**
- **Height**: 20px (h-5)
- **Display**: Flex row, items-center
- **Gap**: 8px (gap-2)
- **Full Width**: self-stretch

**Message Preview:**
- **Flex**: 1 (flex-1)
- **Font**: Lato, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
- **Color**:
  - Default/With Unread: #A3A3A3 (Neutral-400)
  - Active/Selected: #525252 (Neutral-600)
- **Line Clamp**: 1 (line-clamp-1, single line truncation)
- **Example**: "Just confirming my booking for the Mazda 3 next week."

**Unread Badge (with number):**
- **Size**: 20px × 20px (w-5 h-5)
- **Padding**: 4px (p-1)
- **Layout**: Flex column, justify-center, items-center
- **Gap**: 10px (gap-2.5)
- **Inner Container**:
  - Min Width: 16px (min-w-4)
  - Padding: 2px (p-0.5)
  - Background: #FCA5A5 (Red-300)
  - Border Radius: 8px (rounded-lg)
  - Layout: Flex row, justify-center, items-center
  - Gap: 10px (gap-2.5)
- **Number**:
  - Font: Lato, 10px (text-[10px]), Weight 400, Line Height 12px (leading-3)
  - Color: #171717 (Neutral-900)
  - Alignment: Center
  - Example: "5", "12", "99+"
- **Use case**: Unread message count

**Unread Badge (dot only):**
- **Size**: 8px × 8px
- **Background**: #EF4444 (Red-500)
- **Border Radius**: Full (rounded-full)
- **Use case**: Indicator without count

---

#### Chat List Spacing & Alignment

**Container Spacing:**
- **Padding**: 16px all sides (p-4)
- **Gap between items**: 16px (gap-4)
- **Overflow**: Auto scroll for long lists

**Item Spacing:**
- **Padding vertical**: 16px (py-4)
- **Padding horizontal**: 8px (px-2)
- **Gap avatar to content**: 16px (gap-4)
- **Gap between content rows**: 4px (gap-1)
- **Gap in first row**: 8px (gap-2)
- **Gap in second row**: 8px (gap-2)

**Text Alignment:**
- **User name**: Left
- **Badge**: Inline after name
- **Timestamp**: Right
- **Message preview**: Left
- **Unread badge**: Right

---

#### Chat List States & Interactions

**List Item States:**
- **Default**:
  - Transparent background
  - Neutral-900 timestamp
  - Neutral-400 message preview
- **Hover**:
  - Background #FAFAFA or #E5E5E5
  - Cursor pointer
  - Transition 150ms
- **Active/Selected**:
  - Background #F5F5F5
  - Outline 1px solid #86EFAC (Green-300)
  - Zinc-600 timestamp
  - Neutral-600 message preview
- **Pressed**:
  - Background #E5E5E5
  - Scale 0.98
- **With Unread**:
  - Show unread badge
  - Bold or darker text (optional)
  - Neutral-900 timestamp

**Unread Badge States:**
- **Visible**: When unread count > 0
- **Hidden**: When no unread messages (read state)
- **Animation**: Fade in/out, slide in from right

**Avatar States:**
- **Online**: Green ring (outer Rose-200 replaced with Green-200)
- **Offline**: Gray ring or default
- **Busy**: Red ring
- **Away**: Yellow ring

---

#### Chat List Best Practices

**Typography:**
- **User Name**: Lato, 14px, Weight 600, Line Height 16px
- **Badge**: Lato, 12px, Weight 400, Line Height 12px
- **Timestamp**: Lato, 12px, Weight 400, Line Height 12px
- **Message Preview**: Lato, 12px, Weight 400, Line Height 16px
- **Unread Count**: Lato, 10px, Weight 400, Line Height 12px

**Color Coding:**
- **Active Item**: Green-300 outline (#86EFAC)
- **Unread Badge**: Red-300 background (#FCA5A5)
- **Role Badge**: Emerald-100 background (#D1FAE5)
- **Text Colors**: Zinc/Neutral scale for hierarchy

**Spacing:**
- Consistent 16px padding around container
- 16px gap between list items
- 16px gap between avatar and content
- 4px gap between content rows

**Accessibility:**
- Use semantic HTML (ul/li for list)
- Include ARIA labels for unread count
- Keyboard navigation support (arrow keys, Enter to select)
- Focus indicators on active item
- Screen reader announcements for new messages
- High contrast mode support
- Time format in accessible format (aria-label="9:15 AM")

**Responsive Behavior:**
- **Desktop (1024px+)**: Full width 384px with all elements
- **Tablet (768px)**: Slightly narrower, hide badge text on small screens
- **Mobile (320px)**:
  - Reduce padding (p-3 instead of p-4)
  - Hide role badge if space constrained
  - Show timestamp on second line if needed
  - Ensure minimum 44px touch target

**Performance:**
- Virtualize list for 100+ conversations (react-window, react-virtualized)
- Lazy load avatars
- Debounce search/filter input
- Cache recent conversations
- Optimize re-renders (memo, useCallback)

**Common Features:**
- **Search**: Filter by name or message content
- **Sort**: By time, unread, pinned
- **Pin**: Sticky conversations at top
- **Archive**: Hide from main list
- **Delete**: Remove conversation
- **Mute**: Disable notifications
- **Mark as Read/Unread**: Manual status toggle
- **Swipe Actions (mobile)**: Archive, delete, pin

**List Item Variants:**
- **With typing indicator**: Animated "..." below message preview
- **With attachment icon**: Paperclip or image icon before preview
- **Pinned item**: Pin icon, different background, always on top
- **Muted item**: Bell-slash icon, grayed out
- **Group chat**: Multiple avatars or group icon
- **Archived**: Grayed out, "Archived" label

---

#### Chat List Variants

**Simple List (No badges):**
```
[Avatar] Name              Time
         Message preview...
```
- Just name, time, message preview
- No role badge, no unread count
- Use case: Minimal design

**List with Online Status:**
```
[Avatar•] Name    Online   Time
          Message preview...
```
- Green dot on avatar for online status
- Status text inline or as badge
- Use case: Real-time chat applications

**List with Attachments:**
```
[Avatar] Name              Time
         📎 Attachment.pdf  [5]
```
- Icon before message preview
- Show attachment type/name
- Use case: File sharing platforms

**Group Chat List:**
```
[👥] Group Name            Time
     User: Last message... [5]
```
- Group icon instead of single avatar
- Show last sender name
- Use case: Team communication

---

#### Timeline / Activity Feed

**Timeline Container:**
- **Width**: 320px (w-80) example
- **Height**: Auto (based on content)
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Overflow**: Hidden or scroll
- **Background**: #FFFFFF (White)
- **Padding**: 20px (implied from positioning)

---

#### Timeline Item

**Item Container:**
- **Width**: 288px (w-72)
- **Position**: Absolute positioning (left-[20px], top-[20px/112px])
- **Background**: #FFFFFF (White)
- **Layout**: Flex row, items-start
- **Gap**: 12px (gap-3)

---

#### Timeline Elements

**Icon Column (Left):**
- **Layout**: Flex column, items-center
- **Gap**: 4px (gap-1)
- **Padding Bottom**: 4px (pb-1) for items with connecting line
- **Self-stretch**: Full height of item

**Icon Container:**
- **Padding**: 8px (p-2)
- **Background**: #BEF264 (Lime-300)
- **Border Radius**: 20px (rounded-[20px])
- **Gap**: 10px (gap-2.5) internal
- **Overflow**: Hidden
- **Size**: 32px × 32px total (with padding)

**Icon:**
- **Size**: 16px × 16px (w-4 h-4)
- **Color**: #52525B (Zinc-600)
- **Overflow**: Hidden
- **Use case**: Activity type indicator

**Connecting Line (Vertical):**
- **Width**: 0 (w-0)
- **Flex**: 1 (flex-1, fills remaining space)
- **Outline**: 1px solid #E5E5E5 (Neutral-200)
- **Offset**: -0.5px (outline-offset-[-0.50px])
- **Visibility**: Show for all items except last
- **Use case**: Connects timeline events vertically

---

#### Content Column (Right)

**Content Container:**
- **Flex**: 1 (flex-1)
- **Padding Bottom**: 12px (pb-3) for items with connecting line, 0 for last item
- **Layout**: Flex column
- **Gap**: 4px (gap-1) between timestamp and description

**Timestamp:**
- **Font**: Poppins, 10px (text-[10px]), Weight 400, Line Height 12px (leading-3)
- **Color**: #A3A3A3 (Neutral-400)
- **Full Width**: self-stretch
- **Example**: "10:30 AM", "Yesterday", "2 hours ago"

**Description:**
- **Font**: Poppins, 12px (text-xs), Line Height 16px (leading-4)
- **Full Width**: self-stretch
- **Mixed Formatting**:
  - **Title/Action**: Weight 600 (Semibold), Color #27272A (Zinc-800)
  - **Details**: Weight 400 (Normal), Color #27272A (Zinc-800)
- **Example**: "**Cardio progress updated** – 7.5 km completed out of 10 km goal for endurance improvement"
- **Structure**: Bold action text followed by regular detail text

---

#### Timeline Spacing & Layout

**Container Spacing:**
- **Padding**: 20px from edges (left-[20px], top-[20px])
- **Between items**: 92px vertical spacing (112-20 = 92px from top positions)

**Item Spacing:**
- **Icon column to content**: 12px (gap-3)
- **Icon to line**: 4px (gap-1)
- **Timestamp to description**: 4px (gap-1)
- **Item bottom padding**: 12px (pb-3) when connecting line present

**Icon Spacing:**
- **Padding inside icon container**: 8px (p-2)
- **Icon size inside container**: 16px (w-4 h-4)
- **Total icon container**: 32px × 32px

---

#### Timeline States & Interactions

**Item States:**
- **Default**: Normal display with icon, line, and content
- **Hover**: Slight background change (#F7F8F8), cursor pointer (if clickable)
- **Active/Selected**: Background #E8F5FF (Blue-Subtle)
- **Read/Unread**: Bold text for unread, normal for read

**Icon States:**
- **Different Activity Types**: Different background colors
  - Success: Lime-300 (#BEF264)
  - Info: Blue-200 (#BFDBFE)
  - Warning: Yellow-200 (#FEF08A)
  - Error: Red-200 (#FECACA)
  - Default: Neutral-200 (#E5E5E5)

**Connecting Line:**
- **Visible**: All items except last
- **Hidden**: Last item in timeline
- **Color**: Neutral-200 (#E5E5E5)

---

#### Timeline Best Practices

**Typography:**
- **Timestamp**: Poppins, 10px, Weight 400, Line Height 12px
- **Title**: Poppins, 12px, Weight 600, Line Height 16px
- **Description**: Poppins, 12px, Weight 400, Line Height 16px
- **Consistent**: Use Poppins for all timeline text

**Color Coding:**
- **Icon Background**: Lime-300 for success/completion
- **Icon Color**: Zinc-600 for icons
- **Timestamp**: Neutral-400 for subtle appearance
- **Text**: Zinc-800 for good readability
- **Connecting Line**: Neutral-200 for subtle connection

**Spacing:**
- Maintain consistent 12px gap between icon column and content
- Use 4px gap between timestamp and description
- Keep 12px bottom padding on items with connecting lines
- ~92px between timeline items (adjust as needed)

**Accessibility:**
- Use semantic HTML (ol/li for ordered timeline)
- Include time element with datetime attribute
- ARIA labels for activity types
- Keyboard navigation support
- Focus indicators on interactive items
- Screen reader friendly timestamps
- High contrast mode support

**Responsive Behavior:**
- **Desktop (1024px+)**: Full width 320px with all elements
- **Tablet (768px)**: Reduce width slightly
- **Mobile (320px)**:
  - Reduce icon size to 24px (p-1.5 instead of p-2)
  - Smaller font sizes (9px timestamp, 11px description)
  - Reduce spacing between items

**Performance:**
- Virtualize list for 100+ timeline items
- Lazy load old events (infinite scroll)
- Paginate by date ranges
- Cache recent activities
- Optimize icon rendering

**Common Features:**
- **Filtering**: By activity type, date range, user
- **Grouping**: By date (Today, Yesterday, Last Week)
- **Search**: Find specific activities
- **Load More**: Infinite scroll or pagination
- **Real-time Updates**: New items prepended with animation
- **Time Formatting**: Relative (2 hours ago) vs Absolute (10:30 AM)

**Activity Types:**
- **User Actions**: Login, Logout, Profile update
- **System Events**: Backup completed, Sync finished
- **Notifications**: New message, Comment received
- **Progress**: Task completed, Goal achieved
- **Errors**: Failed upload, Connection lost
- **Milestones**: Account created, 100 workouts completed

---

#### Alternate Timeline Layouts

**Compact Timeline Item (Width: 224px):**

Эта вариация использует меньшую ширину и Urbanist шрифт вместо Poppins.

**Container Specs:**
- **Width**: 224px (w-56)
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Padding**: 20px (p-5)
- **Gap**: 20px (gap-5) между элементами
- **Overflow**: Hidden

---

##### Layout Variant 1: Description Above, Timestamp Below

**Item Container:**
- **Width**: 224px (w-56)
- **Layout**: Flex row, items-center
- **Gap**: 14px (gap-3.5)

**Icon Column:**
- **Layout**: Flex column, items-center
- **Gap**: 2px (gap-0.5)
- **Stretch**: self-stretch (full height)

**Icon Container:**
- **Size**: 28px × 28px (w-7 h-7)
- **Background**: #ECFCCB (Lime-200)
- **Border Radius**: 56px (rounded-[56px]) - fully circular
- **Overflow**: Hidden
- **Position**: Relative

**Connecting Line:**
- **Width**: 0 (w-0)
- **Flex**: 1 (flex-1, fills remaining space)
- **Outline**: 1px solid #D6D3D1 (Stone-300)
- **Offset**: -0.5px (outline-offset-[-0.50px])

**Content Column:**
- **Flex**: 1 (flex-1)
- **Padding Top**: 2px (pt-0.5)
- **Padding Bottom**: 10px (pb-2.5)
- **Layout**: Flex column
- **Gap**: 4px (gap-1)

**Description (Name + Action):**
- **Font**: Urbanist, 12px (text-xs), Line Height 16px (leading-4)
- **Name**: Weight 600 (Semibold), Color #27272A (Zinc-800)
- **Action**: Weight 400 (Normal), Color #27272A (Zinc-800)
- **Example**: "**Jamie Smith** updated account settings"
- **Full Width**: self-stretch

**Timestamp (Below Description):**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400, Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Example**: "16:05"

---

##### Layout Variant 2: Timestamp Above, Description Below

**Item Container:**
- **Width**: 224px (w-56)
- **Layout**: Flex row, items-start
- **Gap**: 14px (gap-3.5)

**Icon Container:**
- **Size**: 28px × 28px (w-7 h-7)
- **Background**: #ECFCCB (Lime-200)
- **Border Radius**: 56px (rounded-[56px])
- **Position**: Relative
- **Overflow**: Hidden

**Icon (Inside Container):**
- **Size**: 16px × 16px (w-4 h-4)
- **Position**: Absolute, left 7px, top 7px
- **Overflow**: Hidden

**Icon Graphic:**
- **Size**: 12px × 12px (w-3 h-3)
- **Position**: Absolute, left 2px, top 1px
- **Background**: #27272A (Zinc-800)

**Content Column:**
- **Flex**: 1 (flex-1)
- **Layout**: Flex column
- **Gap**: 2px (gap-0.5)

**Timestamp (Above Description):**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400, Line Height 12px (leading-3)
- **Color**: #737373 (Neutral-500)
- **Example**: "16:05"

**Description (Below Timestamp):**
- **Font**: Urbanist, 12px (text-xs), Line Height 16px (leading-4)
- **Name**: Weight 600 (Semibold), Color #27272A (Zinc-800)
- **Action**: Weight 400 (Normal), Color #27272A (Zinc-800)
- **Example**: "**Jamie Smith** updated account settings"
- **Full Width**: self-stretch

---

**Key Differences Between Layouts:**

| Feature | Layout 1 | Layout 2 |
|---------|----------|----------|
| Timestamp Position | Below description | Above description |
| Icon Column | With connecting line | Single icon only |
| Content Gap | 4px (gap-1) | 2px (gap-0.5) |
| Alignment | items-center | items-start |
| Padding Bottom | 10px (pb-2.5) | None |
| Icon Type | Circle only | Circle with inner icon |

**When to Use:**
- **Layout 1**: Multi-event timeline with chronological flow, emphasizes activity description first
- **Layout 2**: Single events or activity cards, timestamp less important than action

---

#### Timeline Variants

**Compact Timeline:**
```
• Title only
  No connecting line, minimal spacing
```
- Just icon and title, no description
- Smaller spacing between items
- Use case: Quick activity overview

**Timeline with Avatars:**
```
[Avatar] User performed action
  ────── Description details
```
- User avatar instead of icon
- Show who performed the action
- Use case: Social feeds, team activities

**Timeline with Dates:**
```
Today
  • Event 1
  • Event 2
Yesterday
  • Event 3
```
- Group events by date headers
- Date dividers between groups
- Use case: Long timelines spanning days

**Horizontal Timeline:**
```
[Icon] ─── [Icon] ─── [Icon]
Title      Title      Title
```
- Horizontal layout instead of vertical
- Icons connected by horizontal lines
- Use case: Progress steps, milestones

**Rich Timeline:**
```
[Icon] Title              Time
       Description
       [Image/Attachment]
       [Action Buttons]
```
- Include media attachments
- Action buttons (Like, Comment, Share)
- Use case: Social media feeds

---

#### Timeline Icon Categories

**Activity Icons:**
- **Check**: Completed tasks, achievements
- **Bell**: Notifications, reminders
- **User**: Profile updates, mentions
- **Message**: Comments, messages
- **Upload**: File uploads, imports
- **Download**: File downloads, exports
- **Calendar**: Scheduled events, appointments
- **Star**: Favorites, ratings
- **Alert**: Warnings, important notices
- **Info**: General information

**Icon Colors by Type:**
```css
--timeline-success: #BEF264;    /* Lime-300 - Completions */
--timeline-info: #BFDBFE;       /* Blue-200 - Information */
--timeline-warning: #FEF08A;    /* Yellow-200 - Warnings */
--timeline-error: #FECACA;      /* Red-200 - Errors */
--timeline-neutral: #E5E5E5;    /* Neutral-200 - Default */
```

---

### 8. Charts

#### Chart Container

**Main Container:**
- **Width**: 588px (w-[588px])
- **Layout**: Flex column (flex-col)
- **Gap**: 24px (gap-6)
- **Title**:
  - Font: Figtree, 20px (text-xl), Weight 600 (Semibold), Line Height 28px (leading-7)
  - Color: #27272A (Zinc-800)
  - Alignment: Center

**Chart Wrapper:**
- **Padding**: 32px (p-8)
- **Background**: #FAFAF9 (Stone-50)
- **Border Radius**: 12px (rounded-xl)
- **Gap**: 40px (gap-10)
- **Layout**: Flex wrap (flex-wrap)

---

#### Bar Charts

**Chart Container:**
- **Padding**: 20px (p-5)
- **Border**: 1px solid #A855F7 (Purple-500) - для примера/демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Gap**: 20px (gap-5)
- **Layout**: Horizontal flex

**Y-Axis (Vertical Scale):**
- **Height**: 192px (h-48)
- **Gap**: 8px (gap-2)
- **Labels**:
  - Font: Urbanist, 10px, Weight 400, Line Height 12px (leading-3)
  - Color: #27272A (Zinc-800)
  - Padding Right: 8px (pr-2)
  - Example values: "8K", "6K", "4K", "2K", "0"
  - Alignment: Space between (justify-between)

**Bar Column Container:**
- **Width**: 44px (w-11)
- **Height**: 192px (h-48)
- **Border Radius**: 6px (rounded-md)
- **Gap**: 8px (gap-2)

**Grid Lines (Horizontal):**
- **Outline**: 1px solid #E5E5E5 (Neutral-200)
- **Offset**: -0.5px (outline-offset-[-0.50px])
- **Spacing**: Even distribution matching Y-axis labels

**X-Axis Labels:**
- **Font**: Urbanist, 10px, Weight 400, Line Height 12px (leading-3)
- **Color**: #27272A (Zinc-800)
- **Alignment**: Center
- **Example**: "Jan", "Feb", "Mar", etc.

---

#### Bar Types & Variants

**1. Bi-Color Bar (Split Vertical):**
- **Container**: 28px × 160px (w-7 h-40)
- **Layout**: Column flex
- **Top Section**:
  - Background: #164E3F (Teal-900)
  - Border Radius: rounded-tl rounded-tr
  - Padding Top: 36px (pt-9) - determines bar height
- **Bottom Section**:
  - Background: #ECFCCB (Lime-200)
  - Border Radius: rounded-bl rounded-br
  - Padding Bottom: 36px (pb-9) - determines bar height
- **Use case**: Comparison data (positive/negative, profit/loss)

**2. Single Color Bar:**
- **Container**: 32px × 160px (w-8 h-40)
- **Padding Top**: 24px (pt-6) - determines empty space above bar
- **Background**: #ECFCCB (Lime-200)
- **Border Radius**: 6px (rounded-md)
- **Alignment**: Bottom aligned (items-end)
- **Use case**: Simple value representation

**3. Gradient Bar (Split with Transparency):**
- **Container**: 44px × 160px (w-11 h-40)
- **Padding Horizontal**: 8px (px-2)
- **Top Section**:
  - Background: linear-gradient(to bottom, lime-200/25, lime-200/0)
  - Border Top: 1.5px solid #ECFCCB (Lime-200)
  - Padding Top: 36px (pt-9)
- **Bottom Section**:
  - Background: linear-gradient(to left, teal-900/20, teal-900/0)
  - Border Bottom: 1.5px solid #164E3F (Teal-900)
  - Padding Bottom: 36px (pb-9)
- **Use case**: Soft comparison, forecast vs actual

**4. Percentage Bar (with Label):**
- **Container**: 64px × 192px (w-16 h-48)
- **Gap**: 6px (gap-1.5)
- **Outer Padding**: 6px 4px (px-1.5 py-1)
- **Inner Container**:
  - Background: #F4F4F5/60 (Zinc-100 with 60% opacity)
  - Border Radius: 12px (rounded-xl)
  - Padding: 6px (p-1.5)
  - Gap: 4px (gap-1)
- **Percentage Label**:
  - Font: Lato, 9px, Weight 400, Line Height 12px (leading-3)
  - Color: #27272A (Zinc-800)
  - Position: Above bar
  - Example: "110%"
  - Padding Top: 48px (pt-12) - pushes label to specific position
- **Bar**:
  - Background: #ECFCCB (Lime-200)
  - Border Radius: 8px (rounded-lg)
  - Flex: 1 (fills remaining space)
- **Bottom Labels**:
  - Value: Font Lato, 10px, Weight 700 (Bold), Line Height 12px (leading-3), e.g., "2.2 L"
  - Period: Font Urbanist, 10px, Weight 400, Line Height 12px (leading-3), e.g., "Jan"
- **Use case**: Progress indicators, goal tracking

**5. Grouped Bars (2 columns):**
- **Container**: 32px × 160px (w-8 h-40)
- **Padding Vertical**: 6px (py-1.5)
- **Gap**: 4px (gap-1)
- **Layout**: Horizontal flex
- **Bar 1**:
  - Background: #ECFCCB (Lime-200)
  - Padding Top: 12px (pt-3) - determines bar height
  - Border Radius: rounded-tl rounded-tr
  - Flex: 1
- **Bar 2**:
  - Background: #164E3F (Teal-900)
  - Padding Top: 80px (pt-20) - determines bar height
  - Border Radius: rounded-tl rounded-tr
  - Flex: 1
- **Use case**: Side-by-side comparison (e.g., This Year vs Last Year)

**6. Grouped Bars (3 columns):**
- **Container**: 28px × 160px (w-7 h-40)
- **Gap**: 4px (gap-1)
- **Layout**: Horizontal flex
- **Bar 1**:
  - Background: #27272A (Zinc-800)
  - Padding Top: 48px (pt-12)
  - Border Radius: 3px top (rounded-tl-[3px] rounded-tr-[3px])
  - Flex: 1
- **Bar 2**:
  - Background: #ECFCCB (Lime-200)
  - Padding Top: 14px (pt-3.5)
  - Border Radius: 3px top (rounded-tl-[3px] rounded-tr-[3px])
  - Flex: 1
- **Bar 3**:
  - Background: #164E3F (Teal-900)
  - Padding Top: 112px (pt-28)
  - Border Radius: 3px top (rounded-tl-[3px] rounded-tr-[3px])
  - Flex: 1
- **Use case**: Multi-category comparison (e.g., Product A, B, C)

---

#### Area Charts

**Area Chart Container:**
- **Padding**: 20px (p-5)
- **Border**: 1px solid #A855F7 (Purple-500) - для примера
- **Border Radius**: 5px (rounded-[5px])
- **Gap**: 14px (gap-3.5)
- **Layout**: Horizontal flex

**1. Area Chart (Dark Theme):**
- **Width**: 96px (w-24)
- **Height**: 64px (h-16)
- **Position**: Relative
- **Gradient Area**:
  - Background: linear-gradient(to bottom, slate-800/50, slate-800/0)
  - Position: left 1.5px, top 1.39px
  - Full width and height
- **Outline Area**:
  - Height: 44px (h-11) - represents the data area
  - Outline: 2px solid #1E293B (Slate-800)
  - Offset: -1px (outline-offset-[-1px])
  - Position: left 1.5px, top 1.39px
- **Colors**:
  - Main: #1E293B (Slate-800)
  - Gradient: Slate-800/50 to transparent
- **Use case**: Dark/negative trend visualization

**2. Area Chart (Rose Theme, Inverted):**
- **Width**: 96px (w-24)
- **Height**: 64px (h-16)
- **Position**: Relative
- **Gradient Area**:
  - Background: linear-gradient(to bottom, rose-600/40, rose-600/0)
  - Position: left 90.76px, top 63.07px
  - Transform: rotate(180deg), origin top-left
  - Full width and height
- **Outline Area**:
  - Height: 44px (h-11)
  - Outline: 2px solid #E11D48 (Rose-600)
  - Offset: -1px (outline-offset-[-1px])
  - Position: left 90.76px, top 43.59px
  - Transform: rotate(180deg), origin top-left
- **Colors**:
  - Main: #E11D48 (Rose-600)
  - Gradient: Rose-600/40 to transparent
- **Rotation**: 180deg (origin-top-left)
- **Use case**: Inverted trend, decline visualization

---

#### Chart Color Palette

**Primary Colors:**
```css
--chart-teal: #164E3F;        /* Teal-900 - Primary positive */
--chart-lime: #ECFCCB;        /* Lime-200 - Secondary positive */
--chart-zinc: #27272A;        /* Zinc-800 - Neutral/tertiary */
--chart-slate: #1E293B;       /* Slate-800 - Dark theme */
--chart-rose: #E11D48;        /* Rose-600 - Negative/alert */
```

**Gradient Colors:**
```css
--chart-gradient-lime-start: rgba(236, 252, 203, 0.25);  /* Lime-200/25 */
--chart-gradient-lime-end: rgba(236, 252, 203, 0);       /* Lime-200/0 */
--chart-gradient-teal-start: rgba(22, 78, 63, 0.20);     /* Teal-900/20 */
--chart-gradient-teal-end: rgba(22, 78, 63, 0);          /* Teal-900/0 */
--chart-gradient-slate-start: rgba(30, 41, 59, 0.50);    /* Slate-800/50 */
--chart-gradient-slate-end: rgba(30, 41, 59, 0);         /* Slate-800/0 */
--chart-gradient-rose-start: rgba(225, 29, 72, 0.40);    /* Rose-600/40 */
--chart-gradient-rose-end: rgba(225, 29, 72, 0);         /* Rose-600/0 */
```

**Background Colors:**
```css
--chart-bg-light: #F4F4F5;    /* Zinc-100/60 - Light backgrounds */
--chart-bg-grid: #E5E5E5;     /* Neutral-200 - Grid lines */
--chart-text: #27272A;        /* Zinc-800 - Labels and text */
```

---

#### Chart Best Practices

**Typography:**
- **Axis Labels**: Urbanist, 10px, Weight 400, Line Height 12px
- **Data Labels**: Lato, 9-12px, Weight 400-700
- **Chart Title**: Figtree, 20px, Weight 600, Line Height 28px

**Spacing:**
- **Gap between bars**: 4px (grouped), 8px (separate columns)
- **Gap between Y-axis and chart**: 20px (gap-5)
- **Padding inside chart container**: 20px (p-5)
- **Gap between charts**: 40px (gap-10)

**Accessibility:**
- Always include axis labels
- Use high contrast colors (Teal-900, Lime-200 provide good contrast)
- Provide data table alternative for screen readers
- Use patterns/textures in addition to colors for colorblind users

**Responsive Behavior:**
- **Desktop (1024px+)**: Full width charts, all labels visible
- **Tablet (768px)**: Reduce bar width, rotate X-axis labels if needed
- **Mobile (320px)**: Horizontal scroll for wide charts, or stack multiple charts vertically

**Data Ranges:**
- **Y-Axis**: Auto-scale based on data, round to nearest significant figure
- **Bar Heights**: Use padding-top to control (pt-3 to pt-28 range)
- **Percentage Bars**: 0-100% scale, can exceed 100% for over-achievement

---

### 9. Calendar

#### Calendar Container

**Main Container:**
- **Width**: 671px (w-[671px])
- **Layout**: Flex column (flex-col)
- **Gap**: 24px (gap-6)
- **Title**:
  - Font: Figtree, 20px (text-xl), Weight 600 (Semibold), Line Height 28px (leading-7)
  - Color: #27272A (Zinc-800)
  - Alignment: Center

**Calendar Wrapper:**
- **Padding**: 32px (p-8)
- **Background**: #FAFAF9 (Stone-50)
- **Border Radius**: 12px (rounded-xl)
- **Gap**: 40px (gap-10)
- **Layout**: Flex wrap (flex-wrap)

---

#### Date Picker (Mini Calendar)

**Day Header (Mini):**
- **Padding**: 4px 6px (px-1 py-1.5)
- **Border Radius**: 10px (rounded-[10px])
- **Text**:
  - Font: Lato, 10px (text-[10px]), Weight 400, Line Height 12px (leading-3)
  - Color: #A8A29E (Stone-400)
  - Width: 24px (w-6)
  - Alignment: Center
- **Example**: "Wed", "Thu", "Fri"

**Date Picker Row:**
- **Width**: 176px (w-44)
- **Height**: 64px (h-16)
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Layout**: Horizontal flex with absolute positioned cells

**Date Cell (Normal):**
- **Height**: 32px (h-8)
- **Padding**: 4px 5px 6px (px-1 pt-[5px] pb-1.5)
- **Border Radius**: 10px (rounded-[10px])
- **Text**:
  - Font: Lato, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
  - Color: #171717 (Neutral-900)
  - Width: 24px (w-6)
  - Alignment: Center
- **Example**: "30"

**Date Cell (Disabled/Inactive):**
- **Same structure as Normal**
- **Text Color**: #A8A29E (Stone-400)
- **Use case**: Days from previous/next month

**Date Cell (Selected - Rose):**
- **Base**: Same as Normal date cell
- **Background Circle**:
  - Size: 24px × 24px (w-6 h-6)
  - Background: #FECACA (Rose-200)
  - Border Radius: Full (rounded-full)
  - Position: Absolute, left 4px, top 4px
  - Z-index: Behind text
- **Text**: #171717 (Neutral-900), appears above circle
- **Use case**: Event/holiday marked dates

**Date Cell (Selected - Emerald):**
- **Base**: Same as Normal date cell
- **Background Circle**:
  - Size: 24px × 24px (w-6 h-6)
  - Background: #D1FAE5 (Emerald-100)
  - Border Radius: Full (rounded-full)
  - Position: Absolute, left 4px, top 4px
  - Z-index: Behind text
- **Text**: #171717 (Neutral-900), appears above circle
- **Use case**: Today or selected date

---

#### Calendar View (Weekly/Daily)

**Calendar Grid Container:**
- **Width**: 620.67px (w-[620.67px])
- **Height**: 763px (h-[763px])
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Overflow**: Hidden
- **Position**: Relative

---

#### Time Column (Sidebar)

**Time Column Container:**
- **Width**: 80px (w-20)
- **Height**: 723px (h-[723px])
- **Background**: #FFFFFF (White)
- **Layout**: Flex column
- **Position**: Absolute, left 20px, top 20px (first column)
- **Position**: Absolute, left 320.33px, top 20px (middle column with gap)

**Timezone Header:**
- **Height**: 96px (h-24) - for first column
- **Height**: 64px (h-16) - for columns with gap
- **Padding**: 12px 6px (px-1.5 py-3)
- **Background**: #FFFFFF (White)
- **Border Radius**: 16px (rounded-2xl)
- **Text**:
  - Font: Lato, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
  - Color: #4B5563 (Gray-600)
  - Alignment: Center
  - Example: "UTC +1"

**Time Slots Container:**
- **Flex**: 1 (fills remaining space)
- **Padding Top**: 8px (pt-2)
- **Padding Bottom**: 40px (pb-10)
- **Layout**: Flex column, space between (justify-between)

**Time Slot:**
- **Padding**: 8px 14px (px-3.5 py-2)
- **Gap**: 10px (gap-2.5)
- **Text**:
  - Font: Lato, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
  - Color: #52525B (Zinc-600)
  - Alignment: Center
- **Examples**: "9:00 AM", "10:00 AM", "11:00 AM", "12:00 AM", "1:00 PM", "2:00 PM", "3:00 PM"

**Gap between Time Columns:**
- **Gap**: 20px (gap-5) - applies to columns that use gap property

---

#### Day Column

**Day Column Container:**
- **Width**: 176px (w-44)
- **Height**: 723px (h-[723px])
- **Background**: #FFFFFF (White)
- **Layout**: Flex column
- **Overflow**: Hidden
- **Position**: Absolute
  - First day column: left 121px, top 20px
  - Second day column: left 421.33px, top 20px

**Day Header (Active):**
- **Padding**: 12px 6px (px-1.5 py-3)
- **Gap**: 2px (gap-0.5)
- **Inner Container**:
  - Flex: 1
  - Padding: 12px 6px (px-1.5 py-3)
  - Background: #F5F5F5 (Neutral-100)
  - Border Radius: 16px (rounded-2xl)
  - Gap: 4px (gap-1)
  - Layout: Flex column, center aligned
- **Day Label**:
  - Font: Lato, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
  - Color: #52525B (Zinc-600)
  - Alignment: Center
  - Example: "Monday"
- **Date Number**:
  - Font: Lato, 24px (text-2xl), Weight 600 (Semibold), Line Height 28px (leading-7)
  - Color: #171717 (Neutral-900)
  - Alignment: Center
  - Example: "18"

**Day Header (Inactive):**
- **Height**: 64px (h-16) - for columns with gap
- **Padding**: 6px (px-1.5)
- **Gap**: 2px (gap-0.5)
- **Inner Container**:
  - Flex: 1
  - Padding: 12px 6px (px-1.5 py-3)
  - Background: #FFFFFF (White)
  - Border Radius: 16px (rounded-2xl)
  - Gap: 4px (gap-1)
  - Layout: Flex column, center aligned
- **Text Styles**: Same as Active day header
- **Use case**: Non-selected days in multi-day view

**Time Grid Container:**
- **Flex**: 1 (fills remaining space)
- **Padding Top**: 8px (pt-2)
- **Padding Bottom**: 40px (pb-10)
- **Layout**: Flex column, space between (justify-between)

**Grid Line (Hourly):**
- **Height**: 28px (h-7)
- **Padding Vertical**: 8px (py-2)
- **Gap**: 10px (gap-2.5)
- **Border**:
  - Flex: 1
  - Height: 0
  - Outline: 1px solid #E7E5E4 (Stone-200)
  - Offset: -0.5px (outline-offset-[-0.50px])
- **Layout**: Horizontal center (justify-center items-center)

---

#### Calendar States & Interactions

**Day Column States:**
- **Default**: White background, normal border
- **Hover**: Light gray background (#F7F8F8)
- **Selected**: Neutral-100 background in header
- **Today**: Emerald-100 circle behind date number

**Date Cell States:**
- **Default**: No background, Neutral-900 text
- **Hover**: Light background (Stone-100)
- **Disabled**: Stone-400 text color
- **Selected (Today)**: Emerald-100 circle background
- **Selected (Event)**: Rose-200 circle background
- **Active/Clicked**: Scale 0.95, transition 200ms

**Event Blocks** (to be placed on grid):
- **Position**: Absolute positioning over grid lines
- **Width**: Full day column width minus padding
- **Height**: Based on event duration (1 hour = ~100px)
- **Background**: Event category color
- **Border Radius**: 8px (rounded-lg)
- **Padding**: 8px (p-2)
- **Text**: Event title, time, location
- **Shadow**: var(--shadow-sm)

---

#### Calendar Color Coding

**Event Categories:**
```css
--calendar-event-meeting: #43ABFF;      /* Blue-10 - Meetings */
--calendar-event-personal: #ECFCCB;     /* Lime-200 - Personal */
--calendar-event-deadline: #FECACA;     /* Rose-200 - Deadlines */
--calendar-event-holiday: #D1FAE5;      /* Emerald-100 - Holidays */
--calendar-event-blocked: #F5F5F5;      /* Neutral-100 - Blocked time */
```

**Calendar UI Colors:**
```css
--calendar-bg-primary: #FFFFFF;         /* White - Main background */
--calendar-bg-wrapper: #FAFAF9;         /* Stone-50 - Wrapper background */
--calendar-border: #E7E5E4;             /* Stone-200 - Grid lines */
--calendar-text-primary: #171717;       /* Neutral-900 - Dates, headers */
--calendar-text-secondary: #52525B;     /* Zinc-600 - Times, day labels */
--calendar-text-disabled: #A8A29E;      /* Stone-400 - Inactive dates */
--calendar-header-active: #F5F5F5;      /* Neutral-100 - Selected day header */
```

---

#### Calendar Best Practices

**Typography:**
- **Day Names**: Lato, 12px, Weight 400, Line Height 16px
- **Date Numbers (Mini)**: Lato, 12px, Weight 400, Line Height 16px
- **Date Numbers (Large)**: Lato, 24px, Weight 600, Line Height 28px
- **Time Labels**: Lato, 12px, Weight 400, Line Height 16px
- **Timezone**: Lato, 12px, Weight 400, Line Height 16px

**Spacing:**
- **Gap between day columns**: Calculated automatically based on positioning
- **Gap between time columns**: 20px (gap-5)
- **Padding inside calendar wrapper**: 32px (p-8)
- **Grid line spacing**: Auto-distributed based on hour count

**Accessibility:**
- Use semantic HTML (table or grid role)
- Include ARIA labels for dates and events
- Keyboard navigation support (arrow keys to navigate days)
- Focus indicators on interactive elements
- Screen reader announcements for selected dates
- High contrast mode support

**Responsive Behavior:**
- **Desktop (1024px+)**: Full week view with multiple columns
- **Tablet (768px)**: 3-4 day view, reduced column width
- **Mobile (320px)**: Single day view, swipe to navigate

**Time Zone Handling:**
- Always display timezone in header
- Support multiple timezone columns for global teams
- Use UTC offset notation (e.g., "UTC +1", "UTC -5")

**Event Display:**
- Minimum event height: 24px (15-minute minimum)
- Event overlap: Reduce width and show side-by-side
- All-day events: Show in header area above time grid
- Multi-day events: Span across day columns

---

### 10. Avatars

#### Sizes

- **XS**: 24px
- **Small**: 32px
- **Medium**: 40px
- **Large**: 48px
- **XL**: 64px
- **2XL**: 96px

#### Styles

- **Border Radius**: 50% (rounded-full) or 8px (rounded-base for square)
- **Border**: 2px solid #FFFFFF (optional)
- **Placeholder**: Background #F2F3F4, Color #757D83, Font Weight 500
- **Status Indicator**: Size 8px (for Small), 10px (for Medium+), Border 2px solid #FFFFFF, Colors: Success #00C853, Offline #757D83, Busy #FF434E

---

### 11. Toolbars & Filter Bars

#### Toolbar Container

**Main Container:**
- **Width**: 1322px (w-[1322px]) - full width example
- **Height**: Auto (based on content rows)
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Overflow**: Hidden
- **Position**: Relative

**Toolbar Row:**
- **Width**: 1281px (w-[1281px])
- **Layout**: Flex row, space between (justify-between items-center)
- **Gap**: 64px (gap-16) when using flex-1 sections
- **Padding**: 20px from edges (left-[20px], top-[20px/70px/120px/170px])
- **Position**: Absolute

---

#### Toolbar Elements

**Page Title/Header:**
- **Font**: Urbanist, 16px (text-base), Weight 700 (Bold), Line Height 20px (leading-5)
- **Color**: #27272A (Zinc-800)
- **Height**: 16px (h-4)
- **Gap**: 4px (gap-1) in container
- **Use case**: Section or page title

**Search Input (Toolbar):**
- **Width**: 240px (w-60)
- **Padding**: 6px 12px 6px 14px (pl-3.5 pr-3 py-1.5)
- **Background**: #F4F4F5 (Zinc-100)
- **Border**: 1px solid #F4F4F5 (Zinc-100)
- **Outline**: 1px, offset -1px (outline-offset-[-1px])
- **Border Radius**: 16px (rounded-2xl)
- **Gap**: 6px (gap-1.5)
- **Placeholder**:
  - Font: Urbanist, 12px (text-xs), Weight 400, Line Height 16px (leading-4)
  - Color: #737373 (Neutral-500)
  - Example: "Search placeholder"
- **Icon**:
  - Size: 16px (w-4 h-4)
  - Color: #164E3F (Teal-900)
  - Position: Right side
  - Padding: 2px (py-0.5)

**Segmented Button Group:**
- **Width**: 320px (w-80)
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: 8px (rounded-lg)
- **Gap**: 2px (gap-0.5)
- **Layout**: Flex row (3 equal buttons)
- **Button 1 (Active)**:
  - Flex: 1
  - Padding: 12px (px-3 py-2)
  - Background: #164E3F (Teal-900)
  - Border Radius: 8px (rounded-lg)
  - Text: #FAFAFA (Neutral-50), Urbanist 12px Semibold, Line Height 12px (leading-3)
- **Button 2 & 3 (Inactive)**:
  - Flex: 1
  - Padding: 12px (px-3 py-2)
  - Background: #F5F5F4 (Stone-100)
  - Border Radius: 8px (rounded-lg)
  - Text: #164E3F (Teal-900), Urbanist 12px Semibold, Line Height 12px (leading-3)
  - Gap: 2px (gap-0.5)

**Dropdown Button (Ghost with Icon):**
- **Padding**: 12px 8px (pl-3 pr-2 py-2)
- **Border Radius**: 8px (rounded-lg)
- **Outline**: 1px solid #E5E5E5 (Neutral-200), offset -1px (outline-offset-[-1px])
- **Gap**: 4px (gap-1)
- **Overflow**: Hidden
- **Text**:
  - Font: Urbanist, 12px (text-xs), Weight 600 (Semibold), Line Height 12px (leading-3)
  - Color: #164E3F (Teal-900)
  - Padding: 2px (py-0.5)
  - Example: "Popular"
- **Icon (Chevron Down)**:
  - Size: 14px (w-3.5 h-3.5)
  - Color: #164E3F (Teal-900)
  - Padding: 1px (p-px)
  - Position: Right side
- **States**:
  - Hover: Background #F7F8F8 (Gray-BG Subtle)
  - Active: Background #E8F5FF (Blue-Subtle)

**Sort By Group:**
- **Layout**: Flex row, items baseline, Gap 10px (gap-2.5)
- **Label**:
  - Text: "Sort by:"
  - Font: Urbanist, 12px (text-xs), Weight 400, Line Height 12px (leading-3)
  - Color: #737373 (Neutral-500)
- **Dropdown**: Same as Dropdown Button above

**Icon Button (Ghost):**
- **Padding**: 8px (p-2)
- **Border Radius**: 8px (rounded-lg)
- **Outline**: 1px solid #E5E5E5 (Neutral-200), offset -1px
- **Gap**: 8px (gap-2)
- **Icon**:
  - Size: 16px (w-4 h-4)
  - Color: #164E3F (Teal-900)
- **States**:
  - Hover: Background #F7F8F8
  - Active: Background #E8F5FF

**Icon Button (Transparent):**
- **Padding**: 5px (p-[5px])
- **Border Radius**: 6px (rounded-md)
- **Gap**: 8px (gap-2)
- **Icon**:
  - Size: 20px (w-5 h-5)
  - Color: #164E3F (Teal-900)
- **No outline**
- **States**:
  - Hover: Background rgba(22, 78, 63, 0.05)

**Primary Button (Toolbar):**
- **Padding**: 12px (px-3 py-2)
- **Background**: #164E3F (Teal-900)
- **Border Radius**: 8px (rounded-lg)
- **Text**:
  - Font: Urbanist, 12px (text-xs), Weight 600 (Semibold), Line Height 12px (leading-3)
  - Color: #FAFAFA (Neutral-50)
  - Padding: 2px (py-0.5)
- **States**:
  - Hover: Background #0F3D30
  - Active: Background #0A2B21

---

#### Toolbar Layout Patterns

**Pattern 1: Title + Actions (Right-aligned)**
```
┌─────────────────────────────────────────────────┐
│ Header Title          [Search] [Buttons] [...]  │
└─────────────────────────────────────────────────┘
```
- **Left Section**: Page title
- **Right Section**: Search, segmented buttons, dropdowns, icons, primary button
- **Gap**: Space between (justify-between)

**Pattern 2: Search & Filters Left + Actions Right**
```
┌─────────────────────────────────────────────────┐
│ [Search] [Filter] [Filter]    [Actions] [...]   │
└─────────────────────────────────────────────────┘
```
- **Left Section**: Search + filter dropdowns (gap-2.5)
- **Right Section**: More filters, button group, sort, icons, primary button
- **Gap**: Space between

**Pattern 3: Filters Left + Search & Actions Right**
```
┌─────────────────────────────────────────────────┐
│ [Filter] [Filter] [Filter]...  [Sort] [Search]  │
└─────────────────────────────────────────────────┘
```
- **Left Section**: Multiple filter dropdowns (flex-1, gap-2.5)
- **Right Section**: Sort by, button group, search, icons, primary button
- **Gap**: 64px (gap-16)

**Pattern 4: Button Group Left + Full Actions Right**
```
┌─────────────────────────────────────────────────┐
│ [Tab1|Tab2|Tab3]    [Search] [Filters] [Actions]│
└─────────────────────────────────────────────────┘
```
- **Left Section**: Segmented button group (flex-1)
- **Right Section**: Search, icons, filters, sort, primary button
- **Gap**: Space between

---

#### Toolbar Spacing & Alignment

**Container Spacing:**
- **Horizontal padding**: 20px from container edges
- **Vertical spacing between rows**: 50px (70-20, 120-70, 170-120)
- **Internal gap between sections**: 10px (gap-2.5) or 64px (gap-16) for major sections

**Element Spacing:**
- **Between toolbar items**: 10px (gap-2.5) default
- **Between grouped items**: 4px (gap-1) for tightly grouped
- **Between major sections**: 64px (gap-16) when using flex-1

**Alignment:**
- **Default**: items-center (vertical center alignment)
- **Special cases**: items-baseline for "Sort by:" label with dropdown
- **Horizontal**: justify-between for left/right split, justify-start for grouped left

---

#### Toolbar States & Interactions

**Search Input States:**
- **Default**: Zinc-100 background, Neutral-200 border
- **Focus**: Border color #164E3F, Shadow 0 0 0 3px rgba(22, 78, 63, 0.1)
- **Filled**: Show clear icon on right
- **Disabled**: Opacity 0.5, cursor not-allowed

**Dropdown States:**
- **Default**: Neutral-200 outline, Teal-900 text
- **Hover**: Gray-BG Subtle background (#F7F8F8)
- **Active/Open**: Blue-Subtle background (#E8F5FF), chevron rotates 180deg
- **Disabled**: Opacity 0.5

**Icon Button States:**
- **Default**: Neutral-200 outline (ghost) or transparent
- **Hover**: Gray-BG Subtle background
- **Active**: Blue-Subtle background
- **With Badge**: Show notification badge on top-right

**Segmented Buttons States:**
- **Active**: Teal-900 background, Neutral-50 text
- **Inactive**: Stone-100 background, Teal-900 text
- **Hover (inactive)**: Background #E7E5E4 (Stone-200)
- **Disabled**: Opacity 0.5

---

#### Toolbar Best Practices

**Typography:**
- **Title**: Urbanist, 16px, Weight 700, Line Height 20px
- **Button Text**: Urbanist, 12px, Weight 600, Line Height 12px
- **Labels**: Urbanist, 12px, Weight 400, Line Height 12px
- **Placeholder**: Urbanist, 12px, Weight 400, Line Height 16px

**Spacing:**
- Maintain consistent 10px gaps between most elements
- Use 64px gap for major left/right sections
- Keep 20px padding from container edges
- Stack toolbars vertically with 50px spacing

**Accessibility:**
- Use semantic HTML (nav role for navigation toolbars)
- Include ARIA labels for icon-only buttons
- Keyboard navigation support (Tab, Enter, Escape)
- Focus indicators on all interactive elements
- Screen reader announcements for filter changes
- Ensure 44px minimum touch target size on mobile

**Responsive Behavior:**
- **Desktop (1024px+)**: Full horizontal layout as shown
- **Tablet (768px)**: Collapse some elements, 2-row layout
- **Mobile (320px)**: Stack elements vertically, hide less important filters in "More" menu
- Consider hamburger menu for filters on small screens
- Search should remain prominently visible

**Performance:**
- Debounce search input (300-500ms)
- Show loading state when filters are applied
- Update URL params for shareable filter states
- Cache filter options for faster loading

**Common Use Cases:**
- **Data Tables**: Search, column filters, sort, pagination controls, export button
- **E-commerce**: Search, category filters, sort (price, popularity), view toggles (grid/list)
- **Dashboards**: Date range picker, metric selector, refresh button, export data
- **File Browsers**: Search, type filters, sort (name, date, size), view options, upload button
- **Admin Panels**: Search users, role filter, status filter, bulk actions, create new button

---

### 12. List Items

#### List Item

- **Height**: Min 48px (auto with padding)
- **Padding**: 12px 16px
- **Border Bottom**: 1px solid #F2F3F4 (Gray-BG)
- **States**:
  - Hover: Background #F7F8F8 (Gray-BG Subtle)
  - Active: Background #E8F5FF (Blue-Subtle)
  - Selected: Background #E8F5FF (Blue-Subtle), Border-left 3px solid #3384C6 (Blue-00)

---

#### List Item with Color Bar & Stats

Этот компонент используется для отображения категорий с процентным соотношением и суммами (инвестиции, бюджет, portfolio breakdown).

**Container:**
- **Width**: 256px (w-64)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 12px (gap-3)
- **Layout**: Horizontal flex row

**Vertical Color Bar (Left Indicator):**
- **Width**: 16px (w-4)
- **Height**: Full (self-stretch) - растягивается на всю высоту контейнера
- **Background**: #164E3F (Teal-900)
- **Border Radius**: 5px (rounded-[5px])
- **Position**: Left edge
- **Use case**: Визуальный индикатор категории/типа

**Title/Label (Center):**
- **Flex**: 1 (flex-1) - занимает оставшееся пространство
- **Font**: Urbanist, 16px (text-base), Weight 600 (Semibold), Line Height 20px (leading-5)
- **Color**: #27272A (Zinc-800)
- **Alignment**: justify-start
- **Example**: "Mutual Funds", "Stocks", "Real Estate"

**Stats Column (Right):**
- **Display**: Inline-flex, flex-col
- **Alignment**: items-end, justify-center
- **Gap**: 2px (gap-0.5)

**Percentage Value (Top):**
- **Font**: Urbanist, 16px (text-base), Weight 600 (Semibold), Line Height 20px (leading-5)
- **Color**: #27272A (Zinc-800)
- **Alignment**: justify-start
- **Example**: "55%", "30%", "15%"

**Amount Value (Bottom):**
- **Font**: Urbanist, 14px (text-sm), Weight 400 (Normal), Line Height 16px (leading-4)
- **Color**: #737373 (Neutral-500)
- **Alignment**: justify-start
- **Example**: "$275,000", "$150K", "€25,000"

---

**Spacing Breakdown:**
- **Gap between elements**: 12px (gap-3)
- **Color bar to title**: 12px
- **Title to stats**: 12px (автоматически через flex-1)
- **Percentage to amount**: 2px (gap-0.5)

**Color Bar Variants:**

По типу категории:
- **Teal-900** (#164E3F): Mutual Funds, Primary investment
- **Lime-200** (#ECFCCB): Stocks, Growth assets
- **Blue-500** (#3B82F6): Bonds, Fixed income
- **Purple-500** (#A855F7): Real Estate, Property
- **Rose-500** (#F43F5E): Crypto, Alternative assets
- **Zinc-800** (#27272A): Cash, Liquidity
- **Emerald-500** (#10B981): Retirement, Long-term
- **Orange-500** (#F97316): Short-term, Savings

**States:**

**Default:**
- Color bar: Defined category color
- Title: Zinc-800
- Percentage: Zinc-800
- Amount: Neutral-500

**Hover:**
- Background: #F7F8F8 (Gray-BG Subtle)
- Cursor: pointer
- Transition: 150ms ease
- Color bar: Slightly brighter (+10% lightness)

**Active/Selected:**
- Background: #E8F5FF (Blue-Subtle)
- Color bar: 2px outline Blue-500
- Title: Zinc-900 (darker)
- Scale: 0.98

**Disabled:**
- Color bar: Opacity 0.4
- Title: Stone-400
- Percentage: Stone-400
- Amount: Stone-300
- Cursor: not-allowed

---

**Variants:**

**Compact Size (Small):**
- Width: 192px (w-48)
- Color bar: 12px (w-3)
- Gap: 8px (gap-2)
- Title: 14px (text-sm)
- Percentage: 14px (text-sm)
- Amount: 12px (text-xs)

**Default Size (Medium):**
- Width: 256px (w-64)
- Color bar: 16px (w-4)
- Gap: 12px (gap-3)
- Title: 16px (text-base)
- Percentage: 16px (text-base)
- Amount: 14px (text-sm)

**Large Size:**
- Width: 320px (w-80)
- Color bar: 20px (w-5)
- Gap: 16px (gap-4)
- Title: 18px (text-lg)
- Percentage: 18px (text-lg)
- Amount: 16px (text-base)

**With Icon:**
Add icon before title
- Icon size: 20px (w-5 h-5)
- Icon color: Matches color bar
- Gap after icon: 8px (gap-2)

**With Trend Indicator:**
Add up/down arrow next to percentage
- Arrow size: 12px
- Green (#10B981) for up
- Red (#EF4444) for down

**With Progress Bar:**
Add thin progress bar below
- Height: 4px (h-1)
- Background: Neutral-200
- Fill: Matches color bar
- Width: Percentage value

---

**Use Cases:**
- Portfolio breakdown display
- Budget category allocation
- Investment type distribution
- Expense categorization
- Asset allocation overview
- Revenue by category
- Market share visualization

**Best Practices:**
- Keep category names concise (1-2 words)
- Use consistent color coding across related items
- Ensure percentage values add up to 100% when showing complete breakdown
- Format amounts with appropriate currency symbols
- Sort by percentage (descending) for clarity
- Use color bar colors with sufficient contrast
- Group similar categories together

**Accessibility:**
- ARIA role: "listitem" when in a list
- ARIA label: "[Category]: [Percentage], [Amount]"
- Keyboard navigable: Tab to focus, Enter to select
- Focus indicator: 2px outline Teal-900
- Color bar should not be the only indicator (include text)
- Screen reader: announce percentage and amount separately
- Minimum touch target: 48px height

**Layout Patterns:**

**Vertical Stack (List):**
```
[▌] Mutual Funds    55%  $275,000
[▌] Stocks          30%  $150,000
[▌] Bonds           15%   $75,000
```
- Gap between items: 8px (gap-2)
- Container: flex-col

**Grid Layout (2 columns):**
```
[▌] Mutual Funds  55%    [▌] Stocks      30%
    $275,000                 $150,000
[▌] Bonds         15%    [▌] Cash        5%
    $75,000                  $25,000
```
- Grid: 2 columns (grid-cols-2)
- Gap: 12px (gap-3)

**Card Container:**
```
┌─────────────────────────────────┐
│ Portfolio Allocation            │
├─────────────────────────────────┤
│ [▌] Mutual Funds    55% $275K   │
│ [▌] Stocks          30% $150K   │
│ [▌] Bonds           15%  $75K   │
│                                 │
│ Total: $500,000                 │
└─────────────────────────────────┘
```
- Card padding: 20px (p-5)
- List gap: 12px (gap-3)
- Total row: border-top, padding-top

---

#### Stock / Asset List Item

Этот компонент используется для отображения акций, криптовалют или других финансовых активов с текущей ценой и процентным изменением.

**Container:**
- **Width**: 320px (w-80)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 12px (gap-3)
- **Layout**: Horizontal flex row

**Icon Container (Left):**
- **Padding**: 10px (p-2.5)
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: Full (rounded-full) - круглая форма
- **Display**: Flex
- **Alignment**: justify-start, items-start
- **Gap**: 10px (gap-2.5)
- **Size**: 48px × 48px total (with padding)

**Icon/Logo:**
- **Size**: 28px × 28px (w-7 h-7)
- **Position**: Relative
- **Overflow**: Hidden

**Icon Graphic:**
- **Size**: 24px × 24px (w-6 h-6)
- **Position**: Absolute, left 1.75px, top 0
- **Background**: #164E3F (Teal-900)
- **Use case**: Company logo, crypto icon, asset symbol

**Info Column (Center):**
- **Flex**: 1 (flex-1) - занимает оставшееся пространство
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-center
- **Gap**: 4px (gap-1)

**Ticker/Symbol (Top):**
- **Font**: Urbanist, 14px (text-sm), Weight 600 (Semibold), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Full Width**: self-stretch
- **Example**: "GOOGL", "AAPL", "BTC", "ETH"
- **Alignment**: justify-start

**Company Name (Bottom):**
- **Font**: Urbanist, 12px (text-xs), Weight 400 (Normal), Line Height 16px (leading-4)
- **Color**: #737373 (Neutral-500)
- **Alignment**: justify-start
- **Example**: "Microsoft Corporation", "Apple Inc.", "Bitcoin"

**Price Column (Right):**
- **Display**: Inline-flex, flex-col
- **Alignment**: items-end, justify-center
- **Border Radius**: 6px (rounded-md)
- **Gap**: 5px (gap-[5px])

**Price Value (Top):**
- **Font**: Urbanist, 14px (text-sm), Weight 600 (Semibold), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Alignment**: justify-start
- **Example**: "$3,204.50", "€125.30", "₿0.0045"

**Change Indicator Badge (Bottom):**
- **Padding Horizontal**: 5px (px-[5px])
- **Padding Vertical**: 2px (py-0.5)
- **Background**: #ECFCCB (Lime-200) - для положительного изменения
- **Border Radius**: 16px (rounded-2xl) - pill shape
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 4px (gap-1)

**Trend Arrow Icon:**
- **Size**: 10px × 10px (w-2.5 h-2.5)
- **Position**: Relative

**Arrow Graphic:**
- **Size**: 8px × 6px (w-2 h-1.5)
- **Position**: Absolute, left 0.62px, top 2.19px
- **Background**: #27272A (Zinc-800)
- **Direction**: Up arrow (positive), Down arrow (negative)

**Change Percentage Text:**
- **Font**: Urbanist, 10px (text-[10px]), Weight 400, Line Height 12px (leading-3)
- **Color**: #164E3F (Teal-900) - для положительного изменения
- **Example**: "+2.30%", "-1.45%", "+0.05%"

---

**Spacing Breakdown:**
- **Gap between elements**: 12px (gap-3)
- **Icon to info**: 12px
- **Info to price**: 12px (автоматически через flex-1)
- **Ticker to company name**: 4px (gap-1)
- **Price to change badge**: 5px (gap-[5px])
- **Arrow to percentage**: 4px (gap-1)

**Change Indicator Colors:**

**Positive (Up):**
- **Background**: #ECFCCB (Lime-200)
- **Text Color**: #164E3F (Teal-900)
- **Arrow**: Up, Zinc-800
- **Prefix**: "+"

**Negative (Down):**
- **Background**: #FECACA (Red-200) или #FFE1E3 (Red-Subtle)
- **Text Color**: #FF434E (Red) или #DC2626 (Red-600)
- **Arrow**: Down, Red
- **Prefix**: "-"

**Neutral (No Change):**
- **Background**: #F5F5F4 (Stone-100)
- **Text Color**: #737373 (Neutral-500)
- **Arrow**: None или horizontal line
- **Text**: "0.00%"

---

**States:**

**Default:**
- Icon container: Stone-100
- Icon: Teal-900
- Ticker: Zinc-800
- Company: Neutral-500
- Price: Zinc-800
- Change: Lime-200 background (positive)

**Hover:**
- Background: #F7F8F8 (Gray-BG Subtle)
- Cursor: pointer
- Icon container: Stone-200
- Transition: 150ms ease
- Scale: 1.01

**Active/Selected:**
- Background: #E8F5FF (Blue-Subtle)
- Icon container: Blue-100
- Border: 1px solid Blue-300
- Scale: 0.99

**Disabled:**
- Icon container: Stone-50, Opacity 0.5
- Ticker: Stone-400
- Company: Stone-300
- Price: Stone-400
- Change badge: Stone-200, Opacity 0.6
- Cursor: not-allowed

---

**Size Variants:**

**Compact (Small):**
- Width: 256px (w-64)
- Icon container: 40px (p-2), Icon 24px (w-6 h-6)
- Ticker: 12px (text-xs)
- Company: 10px (text-[10px])
- Price: 12px (text-xs)
- Change: 9px (text-[9px])
- Gap: 8px (gap-2)

**Default (Medium):**
- Width: 320px (w-80)
- Icon container: 48px (p-2.5), Icon 28px (w-7 h-7)
- Ticker: 14px (text-sm)
- Company: 12px (text-xs)
- Price: 14px (text-sm)
- Change: 10px (text-[10px])
- Gap: 12px (gap-3)

**Large:**
- Width: 384px (w-96)
- Icon container: 56px (p-3), Icon 32px (w-8 h-8)
- Ticker: 16px (text-base)
- Company: 14px (text-sm)
- Price: 16px (text-base)
- Change: 12px (text-xs)
- Gap: 16px (gap-4)

---

**Enhanced Variants:**

**With Quantity/Shares:**
Add third line in info section
- Text: "125 shares" or "0.5 BTC"
- Font: Urbanist 10px, Stone-400
- Position: Below company name

**With Chart Preview:**
Add mini sparkline chart
- Position: Replace or below change badge
- Size: 60px × 20px
- Color: Matches trend (green/red)

**With Additional Metrics:**
Add more data points
- P/E ratio, Market cap, Volume
- Font: 10px, Neutral-500
- Layout: Grid or horizontal

**With Action Button:**
Add quick action button
- "Buy", "Sell", "Trade"
- Size: 24px × 24px icon button
- Position: Far right
- Color: Teal-900

**With Star/Favorite:**
Add favorite toggle
- Position: Top-right corner of icon container
- Size: 12px star icon
- Colors: Yellow-400 (active), Stone-300 (inactive)

---

**Icon Container Variants:**

**Logo Image:**
- Use actual company logo
- Border radius: rounded-full or rounded-lg
- Background: White or brand color

**Letter Avatar:**
- Display first letter of ticker
- Font: Urbanist 16px Bold
- Background: Generated from ticker (hash color)
- Text: White

**Category Icon:**
- Stock: 📈 or building icon
- Crypto: ₿ or chain icon
- Commodity: 🌾 or resource icon
- ETF: 📊 or fund icon

---

**Use Cases:**
- Stock watchlist
- Portfolio holdings display
- Crypto asset list
- Trading platform asset selection
- Investment tracking
- Market overview
- Favorite stocks/assets
- Real-time price monitoring

**Best Practices:**
- Update prices in real-time or show timestamp
- Use clear color coding for positive/negative changes
- Format prices according to asset type (decimals vary)
- Show ticker prominently for quick recognition
- Include company name for clarity
- Sort by price change, alphabetically, or by holdings
- Provide visual feedback on interactions
- Support pull-to-refresh for price updates

**Accessibility:**
- ARIA role: "listitem" when in a list
- ARIA label: "[Ticker] [Company], Price: [Amount], Change: [Percentage] [up/down]"
- Keyboard navigable: Tab to focus, Enter to select/view details
- Focus indicator: 2px outline Teal-900
- Screen reader: announce price and change separately
- Color should not be the only indicator (use arrows + text)
- Announce updates when prices change (live region)
- Minimum touch target: 48px height

**Layout Patterns:**

**Vertical List (Watchlist):**
```
[○] GOOGL                    $3,204.50
    Microsoft Corporation    +2.30% ↑

[○] AAPL                     $175.43
    Apple Inc.               -0.85% ↓

[○] BTC                      $45,230.00
    Bitcoin                  +5.12% ↑
```
- Gap between items: 12px (gap-3)
- Container: flex-col
- Border bottom: 1px Stone-200

**Grid Layout (2 columns):**
```
[○] GOOGL     $3,204.50    [○] AAPL      $175.43
    MSFT      +2.30% ↑         Apple     -0.85% ↓

[○] BTC       $45,230       [○] ETH       $2,450
    Bitcoin   +5.12% ↑         Ethereum  +3.20% ↑
```
- Grid: 2 columns (grid-cols-2)
- Gap: 16px (gap-4)

**Card Container with Header:**
```
┌──────────────────────────────────────┐
│ My Watchlist              [+ Add]    │
├──────────────────────────────────────┤
│ [○] GOOGL        $3,204.50 +2.30% ↑  │
│ [○] AAPL         $175.43   -0.85% ↓  │
│ [○] BTC          $45,230   +5.12% ↑  │
│                                      │
│ Last updated: 2 minutes ago          │
└──────────────────────────────────────┘
```
- Card padding: 20px (p-5)
- Header: flex row, justify-between
- List gap: 8px (gap-2)
- Footer: text-xs, Neutral-400

**With Grouping:**
```
Stocks
  [○] GOOGL    $3,204.50  +2.30% ↑
  [○] AAPL     $175.43    -0.85% ↓

Crypto
  [○] BTC      $45,230    +5.12% ↑
  [○] ETH      $2,450     +3.20% ↑
```
- Section headers: text-sm, Semibold, Zinc-800
- Spacing: 16px between sections

---

#### Category List Item with Collapse/Expand

Элемент списка категорий с возможностью раскрытия и вертикальными соединительными линиями.

**Container (Demo):**
- **Width**: 320px (w-80)
- **Height**: 240px (h-60) - example height for demo
- **Border**: 1px solid #A855F7 (Purple-500) - для демонстрации
- **Border Radius**: 5px (rounded-[5px])
- **Position**: Relative
- **Overflow**: Hidden

---

**Category Item - Variant 1 (Collapsible with Arrow):**

**Item Container:**
- **Width**: 288px (w-72)
- **Padding**: 14px (p-3.5)
- **Position**: Absolute (left-[20px], top-[20px])
- **Background**: #FAFAFA (Neutral-50)
- **Border Radius**: 16px (rounded-2xl)
- **Outline**: 1px solid #E5E5E5 (Neutral-200)
- **Outline Offset**: -1px (outline-offset-[-1px])
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 14px (gap-3.5)

**Icon Container:**
- **Size**: 28px × 28px (w-7 h-7)
- **Background**: #ECFCCB (Lime-200)
- **Border Radius**: 56px (rounded-[56px]) - fully circular
- **Position**: Relative
- **Overflow**: Hidden

**Icon (Inside):**
- **Size**: 16px × 16px (w-4 h-4)
- **Position**: Absolute, left 7px (centered), top 7px (centered)
- **Overflow**: Hidden

**Icon Graphic:**
- **Size**: 14px × 14px (w-3.5 h-3.5)
- **Position**: Absolute, left 1px, top 1px
- **Background**: #27272A (Zinc-800)

**Category Name:**
- **Flex**: 1 (flex-1)
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-start
- **Gap**: 4px (gap-1)

**Name Text:**
- **Font**: Urbanist, 14px (text-sm), Weight 500 (Medium), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Alignment**: justify-start
- **Example**: "Healthcare", "Finance", "Education"

**Expand/Collapse Arrow:**
- **Padding Vertical**: 2px (py-0.5)
- **Display**: Flex
- **Alignment**: items-center, justify-start
- **Gap**: 10px (gap-2.5)

**Arrow Icon:**
- **Size**: 16px × 16px (w-4 h-4)
- **Position**: Relative

**Arrow Graphic:**
- **Size**: 10px × 6px (w-2.5 h-1.5)
- **Position**: Absolute, left 3.94px, top 6.75px (rotated down)
- **Background**: #164E3F (Teal-900)
- **Direction**: Down (collapsed), Up (expanded)

---

**Category Item - Variant 2 (With Thin Vertical Line):**

**Item Container:**
- **Width**: 288px (w-72)
- **Padding Horizontal**: 14px (px-3.5)
- **Position**: Absolute (left-[20px], top-[98px])
- **Background**: #FAFAFA (Neutral-50)
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 14px (gap-3.5)
- **No border radius** (for list item style)

**Vertical Line Column:**
- **Width**: 28px (w-7)
- **Height**: 56px (h-14)
- **Display**: Flex
- **Alignment**: items-center, justify-center
- **Gap**: 10px (gap-2.5)

**Vertical Line:**
- **Width**: 0 (w-0)
- **Height**: Full (self-stretch)
- **Outline**: 1px solid #D6D3D1 (Stone-300)
- **Outline Offset**: -0.5px (outline-offset-[-0.50px])

**Icon Container:**
- **Size**: 28px × 28px (w-7 h-7)
- **Background**: #F5F5F4 (Stone-100)
- **Border Radius**: 56px (rounded-[56px])
- **Position**: Relative
- **Overflow**: Hidden

**Category Name:**
- Same as Variant 1
- **Font**: Urbanist, 14px (text-sm), Weight 500 (Medium), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)

---

**Category Item - Variant 3 (With Thick Lime Line - Selected):**

**Item Container:**
- **Width**: 288px (w-72)
- **Padding Horizontal**: 14px (px-3.5)
- **Position**: Absolute (left-[20px], top-[172px])
- **Background**: #F5F5F4 (Stone-100) - highlighted background
- **Display**: Inline-flex
- **Alignment**: items-center, justify-start
- **Gap**: 14px (gap-3.5)

**Vertical Line Column:**
- **Width**: 28px (w-7)
- **Height**: 56px (h-14)
- **Display**: Flex
- **Alignment**: items-center, justify-center
- **Gap**: 10px (gap-2.5)

**Vertical Line (Selected):**
- **Width**: 0 (w-0)
- **Height**: Full (self-stretch)
- **Outline**: 4px solid #ECFCCB (Lime-200)
- **Outline Offset**: -2px (outline-offset-[-2px])
- **Use case**: Indicates active/selected category

**Icon Container:**
- **Size**: 28px × 28px (w-7 h-7)
- **Background**: #FAFAFA (Neutral-50) - lighter than list background
- **Border Radius**: 56px (rounded-[56px])
- **Position**: Relative
- **Overflow**: Hidden

---

**Spacing Breakdown:**
- **Gap between icon and name**: 14px (gap-3.5)
- **Vertical line to icon**: Part of same 28px column
- **Item padding**: 14px horizontal
- **Between items**: ~22px vertical (98-20=78, 172-98=74)

**States:**

**Default (Collapsed):**
- Background: Neutral-50 (#FAFAFA)
- Icon container: Lime-200 or Stone-100
- Arrow: Down, Teal-900
- Line: Stone-300 (1px)

**Expanded:**
- Same as default
- Arrow: Up, Teal-900
- Child items visible below

**Selected/Active:**
- Background: Stone-100 (#F5F5F4)
- Line: Lime-200 (4px thick)
- Icon container: Neutral-50 (lighter)

**Hover:**
- Background: #F5F5F5 (Neutral-100)
- Cursor: pointer
- Icon container: Slightly darker
- Transition: 150ms ease

**Pressed:**
- Background: Stone-200
- Scale: 0.99

---

**Vertical Line Variants:**

**Thin Line (Default):**
- Width: 1px
- Color: Stone-300 (#D6D3D1)
- Use case: Regular category items

**Thick Line (Selected):**
- Width: 4px
- Color: Lime-200 (#ECFCCB)
- Use case: Active/selected category

**Dashed Line:**
- Width: 1px
- Style: Dashed (2px dash, 2px gap)
- Color: Stone-300
- Use case: Optional/expandable items

**Gradient Line:**
- Width: 2px
- Gradient: From Lime-200 to transparent
- Use case: Visual hierarchy indicator

**No Line:**
- For last item or standalone items
- Just icon and text

---

**Use Cases:**
- Category navigation with subcategories
- Hierarchical folder structure
- Document tree view
- Menu with nested items
- Tag/category selector
- File explorer
- Org chart display
- Process step indicator

**Best Practices:**
- Show clear visual feedback for collapse/expand state
- Use consistent line thickness for hierarchy level
- Limit nesting to 2-3 levels for usability
- Provide keyboard navigation (Arrow keys, Enter to expand)
- Indicate leaf nodes (no children) differently
- Support drag-and-drop for reordering
- Show item count in collapsed state if relevant
- Animate expand/collapse transitions

**Accessibility:**
- ARIA role: "treeitem" for each item, "tree" for container
- ARIA expanded: "true" or "false" for collapsible items
- ARIA level: Indicate nesting level (1, 2, 3)
- Keyboard navigation: Arrow keys (up/down/left/right), Enter to expand/collapse
- Focus indicator: Clear outline on focused item
- Screen reader: Announce "[Name], tree item, level [N], [expanded/collapsed]"
- Ensure line is decorative (not essential for understanding)

**Layout Patterns:**

**Vertical Tree List:**
```
┌────────────────────────┐
│ ▼ Healthcare           │
│   │ ○ Hospitals        │
│   │ ○ Clinics          │
│ ▼ Finance              │
│   │ ○ Banking          │
└────────────────────────┘
```
- Nested items indented
- Lines connect parent to children
- Expandable parents have arrow

**Flat List with Selection Indicator:**
```
┌────────────────────────┐
│ ─ Healthcare           │
│ ▌ Finance (selected)   │
│ ─ Education            │
└────────────────────────┘
```
- Thick line indicates selection
- No nesting
- Simple category switcher

**With Icon and Count:**
```
┌────────────────────────┐
│ [🏥] Healthcare (15)   │
│ [💰] Finance (8)       │
│ [📚] Education (22)    │
└────────────────────────┘
```
- Category icon on left
- Item count on right
- No vertical lines

---

### 13. Messages / Notifications

#### Toast Notification

- **Width**: Max 400px
- **Padding**: 16px 20px
- **Radius**: 12px (0.75rem / rounded-lg)
- **Shadow**: var(--shadow-lg)
- **Position**: Top-right, 24px from edges
- **Variants**: Success, Error, Warning, Info (using semantic colors)
- **Auto-dismiss**: 5s (Success/Info), 7s (Warning/Error)

#### Alert Banner

- **Padding**: 16px 24px
- **Border Left**: 4px solid (variant color)
- **Background**: Variant subtle background
- **Close Button**: Size 20px, Color #757D83, Position top-right

---

### 14. Panels & Cards

#### Side Panel

- **Width**: 360px (Mobile: 100vw)
- **Background**: #FFFFFF
- **Shadow**: var(--shadow-xl)
- **Padding**: 24px
- **Header**:
  - Padding Bottom: 16px
  - Border Bottom: 1px solid #F2F3F4 (Gray-BG)

#### Modal

- **Max Width**: 600px (Small), 800px (Medium), 1000px (Large)
- **Background**: #FFFFFF
- **Border Radius**: 16px (1rem / rounded-xl)
- **Shadow**: var(--shadow-xl)
- **Overlay**: rgba(0, 14, 25, 0.5)
- **Padding**: 32px (Desktop), 24px (Mobile)

---

#### Contact / User Card

Компактная карточка для отображения контактов, пользователей или участников.

**Container:**
- **Width**: 288px (w-72)
- **Padding**: 14px (p-3.5)
- **Background**: #FAFAFA (Neutral-50)
- **Border Radius**: 16px (rounded-2xl)
- **Outline**: 1px solid #E5E5E5 (Neutral-200)
- **Outline Offset**: -1px (outline-offset-[-1px]) - внутренняя обводка
- **Display**: Inline-flex
- **Alignment**: items-start, justify-start
- **Gap**: 16px (gap-4)

**Avatar (Left):**
- **Size**: 40px × 40px (w-10 h-10)
- **Background**: #ECFCCB (Lime-200)
- **Border Radius**: 24px (rounded-3xl) - почти круглый
- **Position**: Relative
- **Type**: Photo placeholder or user image
- **Style**: Circle

**Info Column (Center):**
- **Flex**: 1 (flex-1) - занимает оставшееся пространство
- **Display**: Inline-flex, flex-col
- **Alignment**: items-start, justify-start
- **Gap**: 4px (gap-1)

**Name/Title:**
- **Font**: Urbanist, 14px (text-sm), Weight 600 (Semibold), Line Height 16px (leading-4)
- **Color**: #27272A (Zinc-800)
- **Alignment**: justify-start
- **Example**: "Audrey Murphy", "John Doe"

**ID/Phone/Email (Subtitle):**
- **Font**: Urbanist, 12px (text-xs), Weight 500 (Medium), Line Height 16px (leading-4)
- **Color**: #737373 (Neutral-500)
- **Alignment**: justify-start
- **Example**: "120987654328", "+1 555-0123", "user@email.com"

---

**Spacing Breakdown:**
- **Container padding**: 14px all sides
- **Avatar to info**: 16px (gap-4)
- **Name to subtitle**: 4px (gap-1)

**States:**

**Default:**
- Background: Neutral-50 (#FAFAFA)
- Outline: Neutral-200 (#E5E5E5)
- Name: Zinc-800
- Subtitle: Neutral-500

**Hover:**
- Background: #F5F5F5 (Neutral-100)
- Outline: Neutral-300 (#D4D4D4)
- Cursor: pointer
- Transition: 150ms ease
- Scale: 1.01

**Active/Selected:**
- Background: #E8F5FF (Blue-Subtle)
- Outline: #3384C6 (Blue-00), 2px
- Shadow: 0 2px 4px rgba(0,0,0,0.05)

**Disabled:**
- Background: #FAFAF9 (Stone-50)
- Outline: Stone-200
- Name: Stone-400
- Subtitle: Stone-300
- Avatar: Opacity 0.5
- Cursor: not-allowed

---

**Variants:**

**With Right Column (Stats/Price):**
Add right-aligned column
- **Right Column**: flex-col, items-end, gap-1
- **Primary Text**: 14px Semibold, Zinc-800 (e.g., "$1,000")
- **Secondary Text**: 12px Medium, Teal-900 (e.g., "Successful")

**With Icon Avatar:**
Replace photo with icon
- **Icon Container**: Same 40px, Lime-200 background
- **Icon**: 20px (w-5 h-5), Zinc-800, centered
- **Position**: Absolute, centered (left-[10px], top-[10px])

**Compact Size:**
- Width: 224px (w-56)
- Padding: 12px (p-3)
- Avatar: 32px (w-8 h-8)
- Gap: 12px (gap-3)
- Name: 12px (text-xs)
- Subtitle: 10px (text-[10px])

**Large Size:**
- Width: 320px (w-80)
- Padding: 16px (p-4)
- Avatar: 48px (w-12 h-12)
- Gap: 16px (gap-4)
- Name: 16px (text-base)
- Subtitle: 14px (text-sm)

**With Actions:**
Add action buttons/icons on right
- **Icon buttons**: 24px, Stone-400
- **Examples**: Edit, Delete, More options
- **Hover**: Teal-900

**With Badge:**
Add status badge
- **Position**: Top-right corner of avatar
- **Size**: 12px dot
- **Colors**: Green (online), Gray (offline), Red (busy)

---

**Avatar Variants:**

**Photo Avatar:**
- Background color as placeholder
- Actual user photo inside
- Border radius: rounded-3xl (24px)

**Letter Avatar:**
- Display initials (e.g., "AM" for Audrey Murphy)
- Font: Urbanist 16px Bold
- Text color: Teal-900
- Background: Lime-200

**Icon Avatar:**
- Generic user icon
- Icon size: 20px
- Icon color: Zinc-800
- Background: Lime-200 or Stone-100

**Color Variations:**
- **Lime-200** (#ECFCCB): Default
- **Blue-100** (#DBEAFE): Info
- **Rose-100** (#FFE4E6): Important
- **Emerald-100** (#D1FAE5): Success
- **Stone-100** (#F5F5F4): Neutral

---

**Use Cases:**
- Contact list display
- User directory
- Team member cards
- Transaction participants
- Chat participants
- Beneficiary selection
- Attendee lists
- Follower/Following lists

**Best Practices:**
- Keep names readable (max 2 lines with ellipsis)
- Format phone numbers/IDs consistently
- Use high-contrast avatars for accessibility
- Provide fallback for missing photos
- Group related cards with consistent spacing
- Support sorting and filtering
- Make entire card clickable for selection

**Accessibility:**
- ARIA role: "article" or "button" if clickable
- ARIA label: "[Name], [ID/Contact info]"
- Keyboard navigable: Tab to focus, Enter to select
- Focus indicator: 2px outline Teal-900
- Screen reader: announce name and contact info separately
- Avatar: alt text with user name
- Minimum touch target: 48px height

**Layout Patterns:**

**Vertical List:**
```
┌──────────────────────────┐
│ [○] Audrey Murphy        │
│     120987654328         │
├──────────────────────────┤
│ [○] John Doe             │
│     120987654329         │
└──────────────────────────┘
```
- Gap: 8px (gap-2)
- Container: flex-col
- Dividers optional

**Grid Layout (2 columns):**
```
[○] Audrey Murphy    [○] John Doe
    120987654328         120987654329

[○] Jane Smith       [○] Bob Wilson
    120987654330         120987654331
```
- Grid: grid-cols-2
- Gap: 12px (gap-3)

**Horizontal Scroll:**
```
[○] User 1  [○] User 2  [○] User 3  →
```
- Display: flex row
- Overflow-x: auto
- Gap: 12px (gap-3)
- Snap scroll optional

---

### 15. Accordion / FAQ

#### Accordion Item

- **Padding**: 16px 20px
- **Border**: 1px solid #DBDDDF (Gray-Line)
- **Border Radius**: 8px (0.5rem / rounded-base)
- **Margin Bottom**: 8px
- **States**:
  - Collapsed: Icon chevron-down, Content hidden
  - Expanded: Icon chevron-up, Background #F7F8F8 (Gray-BG Subtle), Content visible
  - Hover: Background #F7F8F8 (Gray-BG Subtle)

---

### 16. Loading States

#### Skeleton Loader

- **Background**: Linear gradient from #F2F3F4 to #DBDDDF
- **Animation**: Shimmer effect, 1.5s ease-in-out infinite
- **Border Radius**: Matches component (8px for cards, 4px for text lines)
- **Sizes**: Text 16px height, Title 24px height, Avatar circular/square matching avatar sizes

#### Spinner

- **Size**: Small 16px, Medium 24px, Large 32px
- **Color**: #3384C6 (Blue-00) or current text color
- **Animation**: Rotate 360deg, 0.8s linear infinite

---

### 17. Empty States

#### Empty State Layout

- **Icon**: Size 64px, Color #B3B7BA (Gray-10), Style outline
- **Heading**: Font Urbanist, Size 24px, Weight 500, Color #333E47 (Gray-30)
- **Description**: Font Inter, Size 16px, Weight 400, Color #757D83 (Gray-20), Max-width 400px
- **Action Button**: Primary or Secondary button
- **Spacing**:
  - Icon → Heading: 24px
  - Heading → Description: 12px
  - Description → Button: 32px

---

### 18. Special Effects

#### Focus Ring

```css
--focus-ring: 0 0 0 3px rgba(67, 171, 255, 0.1);
--focus-ring-error: 0 0 0 3px rgba(255, 67, 78, 0.1);
```

#### Backdrop Blur

```css
--backdrop-blur-sm: blur(4px);
--backdrop-blur-base: blur(8px);
--backdrop-blur-md: blur(12px);
--backdrop-blur-lg: blur(16px);
```

---

## Паттерны

### Dashboard Layouts

#### Grid Dashboard

- **Grid**: 3 columns (Desktop), 2 columns (Tablet), 1 column (Mobile)
- **Card Spacing**: 24px gap
- **Responsive**: Breakpoints: 1024px (Desktop), 768px (Tablet), 320px (Mobile)

#### Sidebar + Content

- **Sidebar Width**: 240px (Desktop), Collapsed 64px, Hidden on Mobile
- **Content Area**: Flex-grow with max-width 1440px
- **Gap**: 0 (no gap between sidebar and content)
- **Responsive**: Mobile: Sidebar becomes drawer overlay

---

### Form Patterns

#### Single Column Form

- **Max Width**: 600px centered
- **Field Spacing**: 24px between fields
- **Button Group**: Margin-top 32px, Primary button right, Secondary left
- **Layout**: Vertical stack with consistent field widths

#### Multi Column Form

- **Grid**: 2 columns (Desktop), 1 column (Mobile)
- **Full Width Fields**: Textarea, Rich text editor, File upload
- **Responsive**: Breakpoint 768px switches to single column

#### Wizard / Stepper Form

- **Steps Indicator**: Height 48px, Background #F7F8F8, Border-bottom 1px solid #DBDDDF
- **Content Area**: Padding 32px, Min-height 400px
- **Navigation**: Fixed bottom, Padding 16px, Background #FFFFFF, Shadow var(--shadow-sm)
- **Progress**: Active step #3384C6, Completed #00C853, Pending #B3B7BA

---

### Data Visualization

#### Dashboard Card with Chart

- **Header**:
  - Title: Font Urbanist, Size 20px, Weight 500, Color #000E19
  - Subtitle: Font Inter, Size 14px, Weight 400, Color #757D83
  - Actions: Icon buttons or dropdown, Size 32px
- **Chart Area**: Padding 24px, Min-height 300px, Background #FFFFFF
- **Footer**: Padding 16px, Border-top 1px solid #F2F3F4, Font 12px, Color #757D83

#### Table with Filters

- **Filter Bar**:
  - Height: 64px
  - Background: #F7F8F8 (Gray-BG Subtle)
  - Padding: 12px 16px
  - Border Bottom: 1px solid #DBDDDF (Gray-Line)
- **Table**: See Table component specifications
- **Pagination**: Height 48px, Padding 12px 16px, Border-top 1px solid #F2F3F4

---

## Состояния

### Interactive States

#### Default
- Standard appearance with base colors
- Cursor: pointer (for interactive elements)
- Transition: all 0.2s ease-in-out

#### Hover
- Background lightens or darkens by 5-10%
- Shadow increases (if applicable)
- Cursor: pointer
- Smooth transition

#### Active/Focus
- Border: 2px solid #43ABFF (Blue-10)
- Focus ring: var(--focus-ring)
- Scale: 0.98 (for buttons)
- Outline: none (use custom focus ring instead)

#### Disabled
- Opacity: 0.5-0.6
- Cursor: not-allowed
- Background: #F2F3F4 (Gray-BG)
- Color: #B3B7BA (Gray-10)

#### Loading
- Spinner or skeleton loader
- Opacity: 0.7
- Cursor: wait
- Pointer-events: none

#### Error
- Border: 1px solid #FF434E (Red)
- Background: #FFF4F4 (Red-Subtle-2)
- Focus ring: var(--focus-ring-error)
- Icon: Alert Circle, Color #FF434E

#### Success
- Border: 1px solid #00C853 (Success)
- Background: #E8F5E9 (Success-bg)
- Icon: Check Circle, Color #00C853

---

## Иконки

### Icon System

- **Library**: Lucide Icons / Heroicons / Feather Icons (choose one for consistency)
- **Sizes**:
  - XS: 12px
  - SM: 16px
  - Base: 20px
  - MD: 24px
  - LG: 32px
  - XL: 48px
- **Stroke Width**: 2px (default), 1.5px (thin), 2.5px (bold)
- **Style**: Outline (preferred), Solid (for filled states)
- **Color**: Inherits text color by default, can use semantic colors

### Common Icons

| Название | Использование | Размер по умолчанию |
|----------|---------------|---------------------|
| Search | Поисковые поля, поиск по контенту | 20px |
| Close / X | Закрытие модальных окон, удаление тегов | 20px |
| Chevron Down | Выпадающие списки, accordion | 16px |
| Arrow Right | Навигация, ссылки "Подробнее" | 16px |
| Check | Успешные действия, чекбоксы | 20px |
| Alert Circle | Предупреждения, информационные сообщения | 20px |
| X Circle | Ошибки, валидация форм | 20px |
| Menu / Hamburger | Мобильное меню, навигация | 24px |
| User | Профиль пользователя, аватары | 20px |
| Settings | Настройки, параметры | 20px |
| Plus | Добавление элементов, создание | 20px |
| Trash | Удаление элементов | 20px |
| Edit / Pencil | Редактирование контента | 20px |

---

## Как использовать эту дизайн-систему

### Для дизайнеров

1. **Цветовая палитра**: Используйте только цвета из утвержденной палитры. Для новых UI элементов выбирайте из Primary, Semantic или Neutral Colors.
2. **Типографика**: Применяйте Urbanist для заголовков и Inter для основного текста. Соблюдайте иерархию размеров шрифтов.
3. **Spacing**: Используйте шкалу отступов (8px, 16px, 24px, 32px и т.д.) для согласованности.
4. **Компоненты**: Не создавайте новые варианты компонентов без согласования с командой. Используйте существующие компоненты и их состояния.
5. **Файлы Figma/Sketch**: Импортируйте CSS переменные в дизайн-инструменты для автоматической синхронизации.

### Для разработчиков

1. **CSS Переменные**: Импортируйте все CSS переменные в ваш проект. Используйте `var(--color-primary)` вместо хардкода цветов.
2. **Компонентная библиотека**: Создайте переиспользуемые React/Vue компоненты на основе спецификаций компонентов.
3. **Responsive Design**: Используйте брейкпоинты: 320px (Mobile), 768px (Tablet), 1024px (Desktop), 1440px (Large Desktop).
4. **Accessibility**: Соблюдайте контрастность WCAG AA (минимум 4.5:1 для текста), используйте семантический HTML и ARIA атрибуты.
5. **Performance**: Оптимизируйте шрифты (используйте font-display: swap), ленивая загрузка изображений, минификация CSS.

```css
/* Пример использования переменных */
.button-primary {
  background-color: var(--color-primary);
  color: var(--color-white);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-base);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  box-shadow: var(--shadow-button);
  transition: all 0.2s ease-in-out;
}

.button-primary:hover {
  background-color: var(--color-primary-hover);
  box-shadow: var(--shadow-button-hover);
}
```

### Для продуктовой команды

1. **Консистентность UX**: Все новые фичи должны использовать компоненты из дизайн-системы для единообразного пользовательского опыта.
2. **Скорость разработки**: Использование готовых компонентов ускоряет разработку и снижает количество багов.
3. **Коммуникация**: При создании требований ссылайтесь на конкретные компоненты (например, "использовать Primary Button Large").
4. **Обратная связь**: Если существующие компоненты не покрывают ваши потребности, инициируйте обсуждение с дизайн и dev командами.
5. **Документация**: Этот документ - единый источник правды. При несоответствии между макетом и дизайн-системой, приоритет у дизайн-системы.

---

## Поддержка и обновления

**Версия**: 3.0
**Последнее обновление**: 2025
**Контакты**: Для вопросов и предложений обращайтесь к дизайн-команде

### Changelog

- **v3.0** - Полная переработка дизайн-системы с новой цветовой палитрой Blue-Gray и обновленной типографикой
- Добавлены компоненты: Charts, Loading States, Empty States
- Улучшена доступность и responsive дизайн

---
