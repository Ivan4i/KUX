# Motion System + anime.js Implementation

**Status**: Production-Ready | **Framework**: anime.js V4 | **Last Updated**: 2024-12-12

---

## 📑 Table of Contents

1. [Motion Principles](#motion-principles)
2. [Motion Tokens](#motion-tokens)
3. [Animation Presets](#animation-presets)
4. [Architecture](#architecture)
5. [React Hooks](#react-hooks)
6. [Animation Catalog](#animation-catalog)
7. [Performance & Accessibility](#performance--accessibility)
8. [Troubleshooting](#troubleshooting)

---

## Motion Principles

### Goals
- **Purpose-Driven**: Every animation communicates intent, never decorative-only
- **Consistent**: 300ms standard duration, cubic-bezier easing throughout
- **Respectful**: Respects `prefers-reduced-motion` media query
- **Performant**: GPU-accelerated (transform, opacity, filter only)

### Timing Hierarchy
- **Fast** (150ms): micro-interactions, toggles, focus states
- **Normal** (250ms): page transitions, card enters, modals
- **Slow** (350ms): full-screen transitions, complex sequences

---

## Motion Tokens

All motion must use these CSS variables (from V3-DESIGN_SYSTEM.md):

```css
:root {
  /* Duration */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 350ms;

  /* Easing */
  --ease-standard: cubic-bezier(0.16, 1, 0.3, 1);      /* General use */
  --ease-entrance: cubic-bezier(0.34, 1.56, 0.64, 1);  /* Entry animations */
  --ease-exit: cubic-bezier(0.25, 0.46, 0.45, 0.94);   /* Exit animations */
}
```

**anime.js v4 Integration**:

```typescript
import theme from './theme';

const duration = theme.duration.normal;    // 250ms
const easing = theme.easing.entrance;      // cubic-bezier(...)
```

---

## Animation Presets

### Basic Presets

#### Fade
```typescript
anime.targets('.element', {
  opacity: [0, 1],
  duration: theme.duration.normal,
  easing: theme.easing.entrance,
});
```

#### Slide Up
```typescript
anime.targets('.element', {
  translateY: [40, 0],
  opacity: [0, 1],
  duration: theme.duration.normal,
  easing: theme.easing.entrance,
});
```

#### Slide Down
```typescript
anime.targets('.element', {
  translateY: [-40, 0],
  opacity: [0, 1],
  duration: theme.duration.normal,
  easing: theme.easing.entrance,
});
```

#### Slide In (Left)
```typescript
anime.targets('.element', {
  translateX: [-60, 0],
  opacity: [0, 1],
  duration: theme.duration.normal,
  easing: theme.easing.entrance,
});
```

#### Slide In (Right)
```typescript
anime.targets('.element', {
  translateX: [60, 0],
  opacity: [0, 1],
  duration: theme.duration.normal,
  easing: theme.easing.entrance,
});
```

#### Scale Pop
```typescript
anime.targets('.element', {
  scale: [0.85, 1],
  opacity: [0, 1],
  duration: theme.duration.normal,
  easing: theme.easing.entrance,
});
```

#### Rotate Spin
```typescript
anime.targets('.element', {
  rotate: [0, 360],
  duration: 1200,
  easing: 'linear',
  loop: true,
});
```

---

## Architecture

### Engine Setup

```typescript
// src/animation/engine.ts
import anime from 'animejs';

export const animationEngine = {
  get isRunning() {
    return anime.engine.state.running;
  },
  pause() {
    anime.engine.pause();
  },
  play() {
    anime.engine.play();
  },
  subscribe(callback: (time: number) => void) {
    anime.engine.subscribe(callback);
  },
};

// Handle reconnections
window.addEventListener('blur', () => animationEngine.pause());
window.addEventListener('focus', () => animationEngine.play());
```

### Scope-Based Animation

Use `data-scope` to isolate animations by context (room, component, etc.):

```html
<div data-scope="room-123" class="room-container">
  <div class="board-container">...</div>
  <div class="chat-panel">...</div>
  <div class="participants-dock">...</div>
</div>
```

**Cleanup on unmount**:

```typescript
export const cleanupRoomAnimations = (scopeId: string) => {
  const targets = document.querySelectorAll(`[data-scope="${scopeId}"]`);
  targets.forEach((target) => {
    anime.set(target, { opacity: undefined, transform: '' });
  });
};
```

---

## React Hooks

### useAnimeScope

**Purpose**: Isolate animations within a component scope, auto-cleanup on unmount.

```typescript
import { useEffect, useRef } from 'react';
import anime from 'animejs';

interface UseAnimeScopeOptions {
  id: string;
  autoplay?: boolean;
}

export const useAnimeScope = (options: UseAnimeScopeOptions) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const animationsRef = useRef<anime.AnimeInstance[]>([]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    container.dataset.scope = options.id;

    return () => {
      // Cleanup: pause all animations in scope
      animationsRef.current.forEach((anim) => anim.pause());
      animationsRef.current = [];
    };
  }, [options.id]);

  const registerAnimation = (animation: anime.AnimeInstance) => {
    animationsRef.current.push(animation);
    return animation;
  };

  return { containerRef, scopeId: options.id, registerAnimation };
};
```

**Usage**:

```typescript
const MyComponent = () => {
  const { containerRef, scopeId, registerAnimation } = useAnimeScope({
    id: `my-component-${Math.random()}`,
  });

  useEffect(() => {
    const animation = anime.targets(`[data-scope="${scopeId}"] .element`, {
      opacity: [0, 1],
      duration: 300,
    });
    registerAnimation(animation);
  }, [scopeId, registerAnimation]);

  return <div ref={containerRef}>Content</div>;
};
```

### useTimelineAnimation

**Purpose**: Manage timeline-based animations with play/pause/reverse controls.

```typescript
import { useEffect, useRef } from 'react';
import anime from 'animejs';

export const useTimelineAnimation = (
  id: string,
  createTimeline: () => anime.AnimeTimelineInstance
) => {
  const timelineRef = useRef<anime.AnimeTimelineInstance | null>(null);

  useEffect(() => {
    timelineRef.current = createTimeline();
    return () => timelineRef.current?.pause();
  }, [createTimeline]);

  return {
    timeline: timelineRef.current,
    play: () => timelineRef.current?.play(),
    pause: () => timelineRef.current?.pause(),
    reverse: () => timelineRef.current?.reverse(),
  };
};
```

**Usage**:

```typescript
const createRoomEntryTimeline = (scopeId: string) => {
  const timeline = anime.timeline({ autoplay: false });
  
  timeline.add({
    targets: `[data-scope="${scopeId}"] .board-container`,
    opacity: [0, 1],
    duration: theme.duration.normal,
  }, 0);

  return timeline;
};

const MyRoom = ({ roomId }) => {
  const { play } = useTimelineAnimation(
    `room-entry-${roomId}`,
    () => createRoomEntryTimeline(`room-${roomId}`)
  );

  useEffect(() => {
    play();
  }, [play]);

  return <div>Room Content</div>;
};
```

### useDraggable

**Purpose**: Enable draggable elements with anime.js Draggable V4.

```typescript
import { useEffect, useRef } from 'react';
import anime from 'animejs';

interface UseDraggableOptions {
  onDragStart?: () => void;
  onDragEnd?: () => void;
  constrainAxis?: boolean;
}

export const useDraggable = (
  ref: React.RefObject<HTMLElement>,
  options: UseDraggableOptions = {}
) => {
  const draggableRef = useRef<any>(null);

  useEffect(() => {
    if (!ref.current) return;

    draggableRef.current = anime.draggable({
      target: ref.current,
      onDragStart: options.onDragStart,
      onDragEnd: options.onDragEnd,
      constrainAxis: options.constrainAxis,
    });

    return () => draggableRef.current?.reset();
  }, [ref, options]);

  return draggableRef.current;
};
```

---

## Animation Catalog

### Page Transitions

#### Auth → Rooms
**Duration**: 600ms  
**Pattern**: Fade out auth, slide up + fade in rooms, stagger cards

```typescript
export const createAuthToRoomsTimeline = () => {
  const timeline = anime.timeline({ autoplay: false });

  // 1. Fade out auth background
  timeline.add({
    targets: '.auth-background',
    opacity: [1, 0],
    duration: theme.duration.normal,
    easing: theme.easing.exit,
  }, 0);

  // 2. Slide up + fade in rooms list
  timeline.add({
    targets: '.rooms-list',
    opacity: [0, 1],
    translateY: [40, 0],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 300); // 300ms offset

  // 3. Stagger room cards
  timeline.add({
    targets: '.room-card',
    opacity: [0, 1],
    translateY: [20, 0],
    duration: theme.duration.fast,
    easing: theme.easing.entrance,
    delay: anime.stagger(50),
  }, 350);

  return timeline;
};
```

### Room Entry

#### Full Timeline with Sequence
**Duration**: 800ms  
**Elements**: Board (fade), Participants (slide up), Chat (slide in), Stickers (stagger pop)

```typescript
export const createRoomEntranceTimeline = (scopeId: string) => {
  const timeline = anime.timeline({ autoplay: false });

  // 1. Board: fade in
  timeline.add({
    targets: `[data-scope="${scopeId}"] .board-container`,
    opacity: [0, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);

  // 2. Participants: slide up + fade (-150ms offset = overlap)
  timeline.add({
    targets: `[data-scope="${scopeId}"] .participants-dock`,
    translateY: [60, 0],
    opacity: [0, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, -150);

  // 3. Chat: slide in from right (0ms offset = parallel)
  timeline.add({
    targets: `[data-scope="${scopeId}"] .chat-panel`,
    translateX: [300, 0],
    opacity: [0, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);

  // 4. Sticker cards: stagger pop (200ms delay from start)
  timeline.add({
    targets: `[data-scope="${scopeId}"] .participant-tile`,
    scale: [0.8, 1],
    opacity: [0, 1],
    duration: theme.duration.fast,
    easing: theme.easing.entrance,
    delay: anime.stagger(50),
  }, 200);

  return timeline;
};
```

### Presentation Mode

#### Screen Share Focus (Corner Minimize)
**Duration**: 400ms  
**Pattern**: Board shrinks to corner, presentation content scales up, chat dims

```typescript
export const createPresentationModeTimeline = (
  scopeId: string,
  presentationSelector: string
) => {
  const timeline = anime.timeline({ autoplay: false });

  // 1. Board moves to bottom-right corner
  timeline.add({
    targets: `[data-scope="${scopeId}"] .board-container`,
    width: ['100%', '20vw'],
    height: ['100%', '20vh'],
    position: 'fixed',
    right: [0, 0],
    bottom: [0, 0],
    duration: theme.duration.normal,
    easing: theme.easing.standard,
  }, 0);

  // 2. Presentation content scales up
  timeline.add({
    targets: presentationSelector,
    scale: [0.95, 1],
    opacity: [0.8, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);

  // 3. Chat panel dims + becomes inactive
  timeline.add({
    targets: `[data-scope="${scopeId}"] .chat-panel`,
    opacity: [1, 0.2],
    pointerEvents: 'none',
    duration: theme.duration.fast,
    easing: theme.easing.exit,
  }, 0);

  return timeline;
};
```

### Participant Events

#### New Participant Appears
**Duration**: 300ms  
**Pattern**: Scale pop + fade in, staggered by index

```typescript
export const animateNewParticipant = (
  participantElement: HTMLElement,
  index: number
) => {
  return anime.targets(participantElement, {
    scale: [0.7, 1],
    opacity: [0, 1],
    translateY: [30, 0],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
    delay: index * 50,
  });
};
```

#### Speaking Indicator Pulse (VAD Detection)
**Duration**: 200ms loop  
**Pattern**: Expanding halo + scale pulse, stops on silence

```typescript
export const animateSpeakingIndicator = (participantTile: HTMLElement) => {
  const indicator = participantTile.querySelector('.mic-indicator');

  const animation = anime.targets(indicator, {
    boxShadow: [
      `0 0 0 0 ${theme.colors.primary}`,
      `0 0 12px 6px ${theme.colors.primary}`,
    ],
    scale: [1, 1.1],
    duration: 200,
    easing: theme.easing.standard,
    loop: true,
  });

  return {
    stop: () => {
      animation.pause();
      anime.targets(indicator, {
        boxShadow: 'none',
        scale: 1,
        duration: 100,
        easing: theme.easing.exit,
      });
    },
  };
};
```

### Board Interactions

#### Sticky Note Drag Snap
**Duration**: 150ms drag, 250ms snap  
**Pattern**: Draggable with elastic bounce on drop

```typescript
export const setupBoardStickerDragging = (sticker: HTMLElement) => {
  const draggable = anime.draggable({
    target: sticker,
    onDragStart: () => {
      anime.targets(sticker, {
        boxShadow: theme.shadows.lg,
        zIndex: 1000,
        duration: 150,
      });
    },
    onDragEnd: (instance: any) => {
      // Snap to grid (10px)
      const snappedX = Math.round(instance.x / 10) * 10;
      const snappedY = Math.round(instance.y / 10) * 10;

      anime.targets(sticker, {
        translateX: snappedX,
        translateY: snappedY,
        opacity: 1,
        boxShadow: theme.shadows.sm,
        zIndex: 'auto',
        duration: theme.duration.normal,
        easing: 'easeOutElastic(1, 0.6)',
      });

      // Emit position update to server
      socket.emit('updateStickerPosition', {
        stickerId: sticker.dataset.id,
        x: snappedX,
        y: snappedY,
      });
    },
  });

  return draggable;
};
```

### Chat & Panels

#### Chat Panel Toggle
**Duration**: 250ms  
**Pattern**: Slide + fade, both directions

```typescript
export const createChatPanelToggleTimeline = (scopeId: string, isOpening: boolean) => {
  return anime.targets(`[data-scope="${scopeId}"] .chat-panel`, {
    translateX: isOpening ? [300, 0] : [0, 300],
    opacity: isOpening ? [0, 1] : [1, 0],
    duration: theme.duration.normal,
    easing: isOpening ? theme.easing.entrance : theme.easing.exit,
    pointerEvents: isOpening ? 'auto' : 'none',
  });
};
```

### Notifications & Feedback

#### Toast Notification Timeline
**Duration**: 300ms in, 200ms stay, 300ms out  
**Pattern**: Full sequence with auto-dismiss

```typescript
export const createToastNotificationTimeline = (toastElement: HTMLElement) => {
  const timeline = anime.timeline({ autoplay: true });

  // 1. Slide up + fade in (300ms)
  timeline.add({
    targets: toastElement,
    translateY: [40, 0],
    opacity: [0, 1],
    duration: theme.duration.normal,
    easing: theme.easing.entrance,
  }, 0);

  // 2. Stay (3000ms pause, 200ms margin before exit)
  
  // 3. Slide down + fade out (300ms, starts at 3200ms total)
  timeline.add({
    targets: toastElement,
    translateY: [-40, 0],
    opacity: [1, 0],
    duration: theme.duration.normal,
    easing: theme.easing.exit,
  }, 3000); // 3 seconds delay

  return timeline;
};
```

#### Retention Badge Pulse (Critical)
**Duration**: 2000ms loop, color flash at <3 days  
**Pattern**: Pulse + scale + color shift

```typescript
export const animateRetentionBadge = (badgeElement: HTMLElement) => {
  const animation = anime.targets(badgeElement, {
    opacity: [1, 0.6],
    scale: [1, 1.05],
    duration: 2000,
    easing: theme.easing.standard,
    loop: true,
  });

  const daysRemaining = parseInt(badgeElement.dataset.daysRemaining || '30');
  if (daysRemaining < 3) {
    anime.targets(badgeElement, {
      backgroundColor: theme.colors.error,
      color: theme.colors.bg,
      boxShadow: `0 0 12px ${theme.colors.error}`,
    });
  }

  return animation;
};
```

#### File Upload Progress
**Duration**: 2ms per 1% (scales with file size)  
**Pattern**: Smooth linear fill

```typescript
export const animateFileUploadProgress = (
  progressBar: HTMLElement,
  finalProgress: number = 100
) => {
  return anime.targets(
    { value: 0 },
    {
      value: finalProgress,
      easing: 'linear',
      duration: finalProgress * 20, // 2ms per 1%
      update: (instance) => {
        const progress = Math.round(instance.progress * 100);
        progressBar.style.width = `${progress}%`;
        progressBar.textContent = `${progress}%`;
      },
    }
  );
};
```

### Loading States

#### Skeleton Loader Pulse
**Duration**: 1000ms loop  
**Pattern**: Opacity pulse, subtle

```typescript
export const skeletonPulse = anime.timeline({
  autoplay: false,
  loop: true,
});

skeletonPulse.add({
  targets: '.skeleton-loader',
  opacity: [0.5, 1, 0.5],
  duration: 1000,
  easing: 'easeInOutQuad',
});
```

#### Spinner Rotation
**Duration**: 1200ms loop  
**Pattern**: Continuous rotation, linear easing

```typescript
const spinnerAnimation = anime.targets('.spinner', {
  rotate: 360,
  duration: 1200,
  loop: true,
  easing: 'linear',
});
```

---

## Performance & Accessibility

### GPU-Friendly Animations

**Use these properties** (GPU-accelerated):
```css
opacity: 0 → 1
transform: translateX(100px), scale(1.1), rotate(45deg)
filter: blur(5px) → blur(0)
```

**Avoid these** (CPU, layout thrashing):
```css
width: 100px → 200px
height: 100px → 200px
left: 50px → 100px
top: 50px → 100px
padding: 10px → 20px
```

### Best Practices

1. **Batch Animations**: Use timelines for multiple elements, not separate calls
   ```typescript
   // ✓ Good: timeline groups them
   const timeline = anime.timeline();
   timeline.add({ targets: '.a', opacity: 1 });
   timeline.add({ targets: '.b', opacity: 1 });
   ```

2. **Use will-change**: Apply before drag/complex animations
   ```typescript
   export const applyWillChange = (target: HTMLElement, properties: string[]) => {
     target.style.willChange = properties.join(', ');
     setTimeout(() => (target.style.willChange = 'auto'), 300);
   };
   ```

3. **Cleanup on Unmount**: Always pause animations when components unmount
   ```typescript
   useEffect(() => {
     const animation = anime.targets('.element', { opacity: 1 });
     return () => animation.pause();
   }, []);
   ```

4. **Sync with RAF**: Use requestAnimationFrame for custom updates
   ```typescript
   export const syncWithRAF = (callback: () => void) => {
     let rafId: number;
     const tick = () => {
       callback();
       rafId = requestAnimationFrame(tick);
     };
     rafId = requestAnimationFrame(tick);
     return () => cancelAnimationFrame(rafId);
   };
   ```

### Respecting User Preferences

```typescript
export const prefersReducedMotion = () =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export const getAnimationDuration = (normalDuration: number): number => {
  if (prefersReducedMotion()) return 0; // 0–50ms instant feedback
  return normalDuration;
};

export const getAnimationEasing = (normalEasing: string): string => {
  if (prefersReducedMotion()) return 'linear';
  return normalEasing;
};

// Usage
anime.targets('.element', {
  opacity: 1,
  duration: getAnimationDuration(theme.duration.normal),
  easing: getAnimationEasing(theme.easing.entrance),
});
```

### Testing

```typescript
// Jest with fake timers
beforeEach(() => jest.useFakeTimers());
afterEach(() => jest.runOnlyPendingTimers());

test('animation completes', async () => {
  const animation = anime.targets('.element', { opacity: 1, duration: 300 });
  jest.advanceTimersByTime(300);
  expect(animation.progress).toBe(1);
});
```

---

## Troubleshooting

### Q: Animation pauses on disconnect, how to handle reconnection?
**A**: Use engine subscription:
```typescript
socket.on('disconnect', () => animationEngine.pause());
socket.on('connect', () => animationEngine.play());
```

### Q: How do I debug animation timing?
**A**: Log animation progress:
```typescript
const animation = anime.targets('.element', {
  opacity: 1,
  complete: (instance) => console.log('Progress:', instance.progress),
});
```

### Q: Scope animations aren't cleaning up properly?
**A**: Ensure useEffect returns cleanup function:
```typescript
useEffect(() => {
  const animation = anime.targets(`[data-scope="${scopeId}"] .element`, {...});
  return () => animation.pause(); // REQUIRED
}, [scopeId]);
```

### Q: How do I use motion tokens from design system?
**A**: Import and use theme object:
```typescript
import theme from './theme';
anime.targets('.element', {
  duration: theme.duration.normal, // 250ms
  easing: theme.easing.entrance,   // cubic-bezier(...)
});
```

### Q: Performance issue with many animations?
**A**: Limit concurrent animations:
1. Use GPU-friendly properties only (transform, opacity)
2. Batch with timelines instead of individual calls
3. Virtual scroll for large lists
4. Consider CSS animations for simple loops

### Q: How to handle touch/drag on mobile?
**A**: anime.draggable handles touch automatically, but test on device:
```typescript
const draggable = anime.draggable({
  target: element,
  // Works on both mouse and touch events
});
```

---

## Related Documents

- **[V3-DESIGN_SYSTEM.md](V3-DESIGN_SYSTEM.md)** — Color, typography, spacing, component tokens
- **[UX_UI_SPEC.md](UX_UI_SPEC.md)** — Screen layouts, interaction specifications

---

**Last Updated**: 2024-12-12 | **Maintained by**: Frontend Team | **Framework**: anime.js V4
