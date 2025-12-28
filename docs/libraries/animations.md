# Animation Library (Anime.js)

**Location:** `frontend/src/lib/animations/`
**Status:** Parked (excluded from TypeScript compilation until integration)

---

## Overview

Animation framework based on anime.js 4.0+ with React integration.

---

## Documentation Files

| File | Location |
|------|----------|
| README | `frontend/src/lib/animations/README.md` |
| Index | `frontend/src/lib/animations/docs/00-index.md` |
| Foundations | `frontend/src/lib/animations/docs/01-foundations.md` |
| Basics | `frontend/src/lib/animations/docs/02-animation-basics.md` |
| CSS Transforms | `frontend/src/lib/animations/docs/03-css-transforms-properties.md` |
| Values & Types | `frontend/src/lib/animations/docs/04-values-types.md` |
| Timing & Easing | `frontend/src/lib/animations/docs/05-timing-easing.md` |
| Keyframes & Stagger | `frontend/src/lib/animations/docs/06-keyframes-stagger.md` |
| Timeline | `frontend/src/lib/animations/docs/07-timeline.md` |
| Advanced Features | `frontend/src/lib/animations/docs/08-advanced-features.md` |
| SVG & Text | `frontend/src/lib/animations/docs/09-svg-text.md` |
| Utilities | `frontend/src/lib/animations/docs/10-utilities-engine.md` |
| AlignUI Integration | `frontend/src/lib/animations/docs/ANIMATION_INTEGRATION.md` |
| Playbook | `frontend/src/lib/animations/docs/ANIMATION_PLAYBOOK_ANIMEJS.md` |
| Motion Patterns | `frontend/src/lib/animations/docs/MOTION_ANIMEJS.md` |

---

## Directory Structure

```
frontend/src/lib/animations/
├── hooks/
│   ├── useAnimation.ts
│   └── useAnimeMotion.ts
├── utils/
│   ├── animations.ts
│   └── Motion.tsx
└── docs/                    # 14 documentation files
```

---

## Integration

1. Install anime.js:
```bash
cd frontend
npm install animejs
```

2. Remove exclusion from `tsconfig.json` if needed:
```json
// Remove:
"src/lib/animations/**/*"
```

3. Import hooks:
```tsx
import { useAnimation } from '@/lib/animations/hooks/useAnimation';
```

---

## Key Principle

> AlignUI components are NOT modified. Animations are applied via refs only.

---

## See Also

- Main playbook: `ANIMATION_PLAYBOOK_ANIMEJS.md`
- Integration with AlignUI: `ANIMATION_INTEGRATION.md`
