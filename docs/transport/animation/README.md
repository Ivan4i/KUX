# Animation Framework - Anime.js Integration

**Version:** 1.0.0
**Library:** anime.js 4.0+

---

## Contents

- `/docs/` - 14 documentation files covering all anime.js features
- `/hooks/` - React hooks (useAnimation, useAnimeMotion)
- `/utils/` - Animation utilities

## Quick Start

```bash
npm install animejs
cp -r transport/animation/hooks/* /path/to/project/src/hooks/
cp -r transport/animation/utils/* /path/to/project/src/utils/
```

## Basic Usage

```tsx
import { animate } from 'animejs';

animate(element, {
  opacity: [0, 1],
  y: [20, 0],
  duration: 400,
  ease: 'easeOutCubic',
});
```

## Documentation Index

| File | Content |
|------|---------|
| 00-index.md | Documentation index |
| 01-foundations.md | Core concepts |
| 02-animation-basics.md | Basic usage |
| 03-css-transforms-properties.md | CSS transforms |
| 04-values-types.md | Values and types |
| 05-timing-easing.md | Timing and easing |
| 06-keyframes-stagger.md | Keyframes, stagger |
| 07-timeline.md | Timeline control |
| 08-advanced-features.md | Advanced features |
| 09-svg-text.md | SVG and text |
| 10-utilities-engine.md | Utilities |
| ANIMATION_INTEGRATION.md | AlignUI integration |
| ANIMATION_PLAYBOOK_ANIMEJS.md | Complete playbook |
| MOTION_ANIMEJS.md | Motion patterns |

## Key Principle

> AlignUI components are NOT modified. Animations applied via refs only.

---

**Source:** uxcode-meet project
