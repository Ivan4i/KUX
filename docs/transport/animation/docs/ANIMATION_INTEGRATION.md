# Anime.js + AlignUI Integration Guide

**Version:** 1.0
**Last Updated:** 2025-12-18
**Animation Library:** anime.js 4.0+
**UI Library:** AlignUI Design System 2.0
**Pattern:** External animation control via refs, no component modifications

---

## Core Principle

> **AlignUI components MUST NOT be modified.** All animations are applied externally via DOM refs or CSS classes.

---

## Architecture Overview

### Integration Flow
```
AlignUI Component → React Ref → anime.js Target → Animation
                                    ↓
                   anime.js does NOT modify component source
```

### Key Rules

1. **No modifications to `frontend/src/components/alignui/*.tsx`**
2. Use React refs to target AlignUI component DOM nodes
3. Animate CSS transforms (`x`, `y`, `scale`, `rotate`) - NOT layout properties
4. Respect existing CSS transitions in components
5. Use `will-change` for performance hints

---

## Implementation Patterns

### Pattern 1: Ref-based Animation

```tsx
import { useRef, useEffect } from 'react';
import { animate } from 'animejs';
import * as Button from '@/components/alignui/button';

function AnimatedButton() {
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleClick = () => {
    if (buttonRef.current) {
      animate(buttonRef.current, {
        scale: [1, 0.95, 1],
        duration: 200,
        ease: 'easeOutQuad',
      });
    }
  };

  return (
    <Button.Root
      ref={buttonRef}
      onClick={handleClick}
      variant="primary"
      mode="filled"
    >
      Click Me
    </Button.Root>
  );
}
```

### Pattern 2: Container Animation (Recommended)

Wrap AlignUI components in animated containers:

```tsx
import { useRef } from 'react';
import { animate } from 'animejs';
import * as Card from '@/components/alignui/card';

function AnimatedCard({ children }: { children: React.ReactNode }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      animate(containerRef.current, {
        opacity: [0, 1],
        y: [20, 0],
        duration: 400,
        ease: 'easeOutCubic',
      });
    }
  }, []);

  return (
    <div ref={containerRef} style={{ willChange: 'transform, opacity' }}>
      <Card.Root>
        {children}
      </Card.Root>
    </div>
  );
}
```

### Pattern 3: CSS Class Animation Hook

```tsx
import { useCallback, RefObject } from 'react';
import { animate, stagger } from 'animejs';

export function useEntranceAnimation(ref: RefObject<HTMLElement>) {
  const animateIn = useCallback(() => {
    if (ref.current) {
      animate(ref.current, {
        opacity: [0, 1],
        y: [30, 0],
        duration: 500,
        ease: 'easeOutCubic',
      });
    }
  }, [ref]);

  return { animateIn };
}

// Usage
function MyComponent() {
  const cardRef = useRef<HTMLDivElement>(null);
  const { animateIn } = useEntranceAnimation(cardRef);

  useEffect(() => {
    animateIn();
  }, [animateIn]);

  return <div ref={cardRef}>...</div>;
}
```

---

## Animation Categories for AlignUI

### 1. Page Transitions

```tsx
// Page entrance animation
export function usePageEntrance() {
  const pageRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (pageRef.current) {
      animate(pageRef.current, {
        opacity: [0, 1],
        duration: 300,
        ease: 'easeOutQuad',
      });
    }
  }, []);

  return pageRef;
}
```

### 2. List Stagger Animations

```tsx
import { animate, stagger } from 'animejs';

// Animate list items appearing
export function animateListEntrance(containerSelector: string) {
  animate(`${containerSelector} > *`, {
    opacity: [0, 1],
    y: [20, 0],
    delay: stagger(50, { start: 100 }),
    duration: 400,
    ease: 'easeOutCubic',
  });
}

// Usage with AlignUI components
function RoomList({ rooms }: { rooms: Room[] }) {
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (rooms.length > 0) {
      animateListEntrance('.room-list');
    }
  }, [rooms]);

  return (
    <div ref={listRef} className="room-list flex flex-col gap-4">
      {rooms.map(room => (
        <RoomCard key={room.id} room={room} />
      ))}
    </div>
  );
}
```

### 3. Modal/Drawer Animations

AlignUI modals use Radix UI with built-in animations. To enhance:

```tsx
// Don't override Radix animations - enhance overlay/content
export function useModalAnimation(isOpen: boolean) {
  const overlayRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen && contentRef.current) {
      // Enhance with spring animation
      animate(contentRef.current, {
        scale: [0.95, 1],
        duration: 300,
        ease: 'spring(1, 100, 10)',
      });
    }
  }, [isOpen]);

  return { overlayRef, contentRef };
}
```

### 4. Button Feedback

```tsx
// Click feedback without modifying Button.tsx
export function useButtonFeedback() {
  const buttonRef = useRef<HTMLButtonElement>(null);

  const triggerFeedback = useCallback(() => {
    if (buttonRef.current) {
      animate(buttonRef.current, {
        scale: [1, 0.97, 1],
        duration: 150,
        ease: 'easeOutQuad',
      });
    }
  }, []);

  return { buttonRef, triggerFeedback };
}
```

### 5. Loading States

```tsx
// Infinite loader animation
export function useLoaderAnimation(ref: RefObject<HTMLElement>) {
  useEffect(() => {
    if (ref.current) {
      const anim = animate(ref.current, {
        rotate: 360,
        duration: 1000,
        loop: true,
        ease: 'linear',
      });

      return () => anim.pause();
    }
  }, [ref]);
}
```

### 6. Number/Counter Animation

```tsx
import { animate } from 'animejs';

export function animateCounter(
  element: HTMLElement,
  from: number,
  to: number,
  duration = 1000
) {
  const counter = { value: from };

  animate(counter, {
    value: to,
    duration,
    ease: 'easeOutQuad',
    onUpdate: () => {
      element.textContent = Math.round(counter.value).toString();
    },
  });
}
```

---

## Safe Animation Properties

### DO Animate (Transform-based, GPU accelerated)
```typescript
// These won't trigger layout thrashing
const safeProperties = {
  x: 100,           // translateX
  y: 50,            // translateY
  z: 0,             // translateZ
  scale: 1.1,       // scale
  scaleX: 1,        // scaleX
  scaleY: 1,        // scaleY
  rotate: 45,       // rotate (deg)
  rotateX: 0,       // rotateX
  rotateY: 0,       // rotateY
  opacity: 0.5,     // opacity (not layout)
  skewX: 0,         // skewX
  skewY: 0,         // skewY
};
```

### AVOID Animating (Layout-triggering)
```typescript
// These trigger expensive layout recalculations
const avoidProperties = {
  width: '100px',    // Use scaleX instead
  height: '50px',    // Use scaleY instead
  top: '10px',       // Use y instead
  left: '20px',      // Use x instead
  margin: '10px',    // Causes reflow
  padding: '5px',    // Causes reflow
  fontSize: '16px',  // Causes reflow
};
```

---

## Timing Recommendations for AlignUI

### Duration Guidelines

| Animation Type | Duration | Ease |
|---------------|----------|------|
| Micro-interaction | 100-200ms | `easeOutQuad` |
| Button feedback | 150-200ms | `easeOutQuad` |
| List item entrance | 300-400ms | `easeOutCubic` |
| Page transition | 200-400ms | `easeOutQuad` |
| Modal open | 250-350ms | `spring(1, 100, 10)` |
| Drawer slide | 300-400ms | `easeOutCubic` |
| Tooltip | 150-200ms | `easeOutQuad` |

### Stagger Guidelines

| Element Count | Stagger Delay | Total Duration |
|---------------|---------------|----------------|
| 3-5 items | 50ms | ~400ms total |
| 6-10 items | 40ms | ~600ms total |
| 10+ items | 30ms | ~800ms max |

---

## Integration with AlignUI Tokens

### Using Token Values in Animations

```tsx
import { animate } from 'animejs';

// Get CSS variable value
function getCSSVar(varName: string): string {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(varName).trim();
}

// Animate to token colors
function animateToErrorState(element: HTMLElement) {
  animate(element, {
    backgroundColor: getCSSVar('--color-error-lighter'),
    borderColor: getCSSVar('--color-error-base'),
    duration: 200,
    ease: 'easeOutQuad',
  });
}
```

### Respecting Existing Transitions

AlignUI components have built-in `transition duration-200 ease-out` classes. Don't conflict:

```tsx
// BAD: Fighting with CSS transitions
animate(button, {
  backgroundColor: '#ff0000',  // AlignUI manages this via hover states
  duration: 200,
});

// GOOD: Only animate transform properties
animate(button, {
  scale: 0.98,
  duration: 150,
});
```

---

## React Hook Library

### useAnimate Hook

```tsx
import { useRef, useCallback, RefObject } from 'react';
import { animate, type AnimationParams } from 'animejs';

export function useAnimate<T extends HTMLElement>(): [
  RefObject<T>,
  (params: AnimationParams) => void
] {
  const ref = useRef<T>(null);

  const run = useCallback((params: AnimationParams) => {
    if (ref.current) {
      animate(ref.current, params);
    }
  }, []);

  return [ref, run];
}

// Usage
function MyComponent() {
  const [buttonRef, animateButton] = useAnimate<HTMLButtonElement>();

  return (
    <Button.Root
      ref={buttonRef}
      onClick={() => animateButton({ scale: [1, 0.95, 1], duration: 200 })}
    >
      Click
    </Button.Root>
  );
}
```

### useStaggeredList Hook

```tsx
import { useEffect } from 'react';
import { animate, stagger } from 'animejs';

export function useStaggeredList(
  selector: string,
  deps: unknown[] = []
) {
  useEffect(() => {
    const elements = document.querySelectorAll(selector);
    if (elements.length > 0) {
      animate(elements, {
        opacity: [0, 1],
        y: [20, 0],
        delay: stagger(50),
        duration: 400,
        ease: 'easeOutCubic',
      });
    }
  }, deps);
}
```

### useScrollAnimation Hook

```tsx
import { useEffect, RefObject } from 'react';
import { animate } from 'animejs';

export function useScrollAnimation(
  ref: RefObject<HTMLElement>,
  options: {
    threshold?: number;
    rootMargin?: string;
  } = {}
) {
  useEffect(() => {
    if (!ref.current) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animate(entry.target as HTMLElement, {
              opacity: [0, 1],
              y: [30, 0],
              duration: 500,
              ease: 'easeOutCubic',
            });
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: options.threshold ?? 0.1,
        rootMargin: options.rootMargin ?? '0px',
      }
    );

    observer.observe(ref.current);

    return () => observer.disconnect();
  }, [ref, options.threshold, options.rootMargin]);
}
```

---

## Complete Example: Animated Room Card

```tsx
import { useRef, useCallback } from 'react';
import { animate } from 'animejs';
import * as Avatar from '@/components/alignui/avatar';
import * as Badge from '@/components/alignui/badge';
import * as Button from '@/components/alignui/button';
import { RiPlayLine } from '@remixicon/react';

interface Room {
  id: string;
  name: string;
  participants: number;
  isLive: boolean;
}

export function RoomCard({ room, index }: { room: Room; index: number }) {
  const cardRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // Entrance animation with stagger based on index
  useEffect(() => {
    if (cardRef.current) {
      animate(cardRef.current, {
        opacity: [0, 1],
        y: [20, 0],
        delay: index * 50 + 100,
        duration: 400,
        ease: 'easeOutCubic',
      });
    }
  }, [index]);

  // Hover animation
  const handleHover = useCallback(() => {
    if (cardRef.current) {
      animate(cardRef.current, {
        scale: 1.02,
        duration: 200,
        ease: 'easeOutQuad',
      });
    }
  }, []);

  const handleHoverEnd = useCallback(() => {
    if (cardRef.current) {
      animate(cardRef.current, {
        scale: 1,
        duration: 200,
        ease: 'easeOutQuad',
      });
    }
  }, []);

  // Click feedback
  const handleButtonClick = useCallback(() => {
    if (buttonRef.current) {
      animate(buttonRef.current, {
        scale: [1, 0.95, 1],
        duration: 150,
        ease: 'easeOutQuad',
      });
    }
  }, []);

  return (
    <div
      ref={cardRef}
      className="rounded-20 border border-stroke-soft-200 bg-bg-white-0 p-4"
      style={{ opacity: 0, willChange: 'transform, opacity' }}
      onMouseEnter={handleHover}
      onMouseLeave={handleHoverEnd}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Avatar.Root size="40" color="blue">
            <Avatar.Indicator position="bottom">
              <Avatar.Status status={room.isLive ? 'online' : 'offline'} />
            </Avatar.Indicator>
          </Avatar.Root>
          <div>
            <h3 className="text-label-md text-text-strong-950">{room.name}</h3>
            <p className="text-paragraph-xs text-text-sub-600">
              {room.participants} participants
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {room.isLive && (
            <Badge.Root variant="light" color="green" size="small">
              <Badge.Dot />
              <span>Live</span>
            </Badge.Root>
          )}

          <Button.Root
            ref={buttonRef}
            variant="primary"
            mode="filled"
            size="small"
            onClick={handleButtonClick}
          >
            <Button.Icon as={RiPlayLine} />
            <span>Join</span>
          </Button.Root>
        </div>
      </div>
    </div>
  );
}
```

---

## Performance Best Practices

### 1. Use `will-change` Wisely

```tsx
// Apply to elements that will animate
<div style={{ willChange: 'transform, opacity' }}>
  {/* Animated content */}
</div>

// Remove after animation completes
animation.then(() => {
  element.style.willChange = 'auto';
});
```

### 2. Batch Animations

```tsx
// BAD: Multiple animate calls
elements.forEach(el => animate(el, { x: 100 }));

// GOOD: Single animate call with array
animate(elements, {
  x: 100,
  delay: stagger(50)
});
```

### 3. Clean Up Animations

```tsx
useEffect(() => {
  const anim = animate(ref.current, {
    rotate: 360,
    loop: true,
  });

  return () => {
    anim.pause();   // Stop animation
    anim.reset();   // Reset to initial state
  };
}, []);
```

### 4. Respect `prefers-reduced-motion`

```tsx
function useReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function AnimatedComponent() {
  const reducedMotion = useReducedMotion();

  useEffect(() => {
    if (reducedMotion) return;  // Skip animations

    animate(ref.current, {
      opacity: [0, 1],
      duration: 400,
    });
  }, [reducedMotion]);
}
```

---

## Verification Commands

```bash
# Check anime.js is installed
grep "animejs" frontend/package.json

# Find existing animation usage
grep -r "animate(" frontend/src/

# Check for transition conflicts
grep "transition" frontend/src/components/alignui/*.tsx

# Find ref usage patterns
grep -r "useRef" frontend/src/pages/*.tsx
```

---

## Summary

| Aspect | Rule |
|--------|------|
| Component Modification | NEVER modify AlignUI components |
| Animation Target | Use refs or wrapper containers |
| Properties | Prefer transforms over layout properties |
| Duration | 150-400ms for most UI animations |
| Ease | `easeOutQuad` for entrances, `easeOutCubic` for exits |
| Cleanup | Always clean up infinite/looping animations |
| Accessibility | Respect `prefers-reduced-motion` |

---

**Document Status:** Ready for agent consumption
**Maintenance:** Update when new animation patterns are established
