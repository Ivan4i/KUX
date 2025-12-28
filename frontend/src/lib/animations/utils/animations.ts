/**
 * Animation Utilities using anime.js
 * Reusable animation patterns for consistent micro-interactions
 */

import anime from 'animejs';

// Animation duration presets (matches AlignUI timing)
export const DURATION = {
  fast: 150,
  normal: 300,
  slow: 500,
  slower: 700,
} as const;

// Easing presets
export const EASING = {
  entrance: 'easeOutCubic',
  exit: 'easeInCubic',
  spring: 'spring(1, 80, 10, 0)',
  bounce: 'easeOutElastic(1, 0.5)',
  smooth: 'easeInOutQuad',
} as const;

/**
 * Fade in animation
 */
export function fadeIn(
  element: Element | Element[] | string | null,
  options?: {
    duration?: number;
    delay?: number;
    easing?: string;
    translateY?: number;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const {
    duration = DURATION.normal,
    delay = 0,
    easing = EASING.entrance,
    translateY = 20,
  } = options || {};

  return anime({
    targets: element,
    opacity: [0, 1],
    translateY: [translateY, 0],
    duration,
    delay,
    easing,
  });
}

/**
 * Fade out animation
 */
export function fadeOut(
  element: Element | Element[] | string | null,
  options?: {
    duration?: number;
    delay?: number;
    easing?: string;
    translateY?: number;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const {
    duration = DURATION.normal,
    delay = 0,
    easing = EASING.exit,
    translateY = -20,
  } = options || {};

  return anime({
    targets: element,
    opacity: [1, 0],
    translateY: [0, translateY],
    duration,
    delay,
    easing,
  });
}

/**
 * Scale in animation (for modals, popovers)
 */
export function scaleIn(
  element: Element | Element[] | string | null,
  options?: {
    duration?: number;
    delay?: number;
    scale?: number;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const { duration = DURATION.normal, delay = 0, scale = 0.95 } = options || {};

  return anime({
    targets: element,
    opacity: [0, 1],
    scale: [scale, 1],
    duration,
    delay,
    easing: EASING.entrance,
  });
}

/**
 * Scale out animation
 */
export function scaleOut(
  element: Element | Element[] | string | null,
  options?: {
    duration?: number;
    delay?: number;
    scale?: number;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const { duration = DURATION.fast, delay = 0, scale = 0.95 } = options || {};

  return anime({
    targets: element,
    opacity: [1, 0],
    scale: [1, scale],
    duration,
    delay,
    easing: EASING.exit,
  });
}

/**
 * Slide in from direction
 */
export function slideIn(
  element: Element | Element[] | string | null,
  direction: 'left' | 'right' | 'up' | 'down' = 'right',
  options?: {
    duration?: number;
    delay?: number;
    distance?: number;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const { duration = DURATION.normal, delay = 0, distance = 100 } = options || {};

  const translateMap = {
    left: { translateX: [-distance, 0], translateY: 0 },
    right: { translateX: [distance, 0], translateY: 0 },
    up: { translateX: 0, translateY: [-distance, 0] },
    down: { translateX: 0, translateY: [distance, 0] },
  };

  return anime({
    targets: element,
    opacity: [0, 1],
    ...translateMap[direction],
    duration,
    delay,
    easing: EASING.entrance,
  });
}

/**
 * Slide out to direction
 */
export function slideOut(
  element: Element | Element[] | string | null,
  direction: 'left' | 'right' | 'up' | 'down' = 'right',
  options?: {
    duration?: number;
    delay?: number;
    distance?: number;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const { duration = DURATION.fast, delay = 0, distance = 100 } = options || {};

  const translateMap = {
    left: { translateX: [0, -distance], translateY: 0 },
    right: { translateX: [0, distance], translateY: 0 },
    up: { translateX: 0, translateY: [0, -distance] },
    down: { translateX: 0, translateY: [0, distance] },
  };

  return anime({
    targets: element,
    opacity: [1, 0],
    ...translateMap[direction],
    duration,
    delay,
    easing: EASING.exit,
  });
}

/**
 * Button press effect
 */
export function buttonPress(
  element: Element | Element[] | string | null
): anime.AnimeInstance | null {
  if (!element) return null;

  return anime({
    targets: element,
    scale: [1, 0.95, 1],
    duration: DURATION.fast,
    easing: EASING.smooth,
  });
}

/**
 * Shake animation (for errors)
 */
export function shake(
  element: Element | Element[] | string | null,
  options?: {
    intensity?: number;
    duration?: number;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const { intensity = 10, duration = DURATION.slow } = options || {};

  return anime({
    targets: element,
    translateX: [0, -intensity, intensity, -intensity, intensity, 0],
    duration,
    easing: 'easeInOutSine',
  });
}

/**
 * Pulse animation (for attention)
 */
export function pulse(
  element: Element | Element[] | string | null,
  options?: {
    scale?: number;
    duration?: number;
    loop?: boolean | number;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const { scale = 1.05, duration = DURATION.slow, loop = false } = options || {};

  return anime({
    targets: element,
    scale: [1, scale, 1],
    duration,
    easing: EASING.smooth,
    loop,
  });
}

/**
 * Stagger animation for lists
 */
export function staggerIn(
  elements: Element[] | NodeListOf<Element> | string | null,
  options?: {
    duration?: number;
    staggerDelay?: number;
    translateY?: number;
    delay?: number;
  }
): anime.AnimeInstance | null {
  if (!elements) return null;

  const {
    duration = DURATION.normal,
    staggerDelay = 50,
    translateY = 20,
    delay = 0,
  } = options || {};

  return anime({
    targets: elements,
    opacity: [0, 1],
    translateY: [translateY, 0],
    duration,
    delay: anime.stagger(staggerDelay, { start: delay }),
    easing: EASING.entrance,
  });
}

/**
 * Typewriter effect
 */
export function typewriter(
  element: HTMLElement | null,
  text: string,
  options?: {
    duration?: number;
    onComplete?: () => void;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const { duration = 50, onComplete } = options || {};

  element.textContent = '';

  return anime({
    targets: { chars: 0 },
    chars: text.length,
    duration: duration * text.length,
    easing: 'linear',
    round: 1,
    update: (anim) => {
      const currentVal = anim.animations[0].currentValue;
      const progress = Math.round(typeof currentVal === 'number' ? currentVal : parseFloat(String(currentVal)) || 0);
      element.textContent = text.slice(0, progress);
    },
    complete: onComplete,
  });
}

/**
 * Number counter animation
 */
export function countUp(
  element: HTMLElement | null,
  endValue: number,
  options?: {
    startValue?: number;
    duration?: number;
    decimals?: number;
    prefix?: string;
    suffix?: string;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const {
    startValue = 0,
    duration = DURATION.slow,
    decimals = 0,
    prefix = '',
    suffix = '',
  } = options || {};

  return anime({
    targets: { value: startValue },
    value: endValue,
    duration,
    easing: EASING.entrance,
    round: decimals === 0 ? 1 : Math.pow(10, decimals),
    update: (anim) => {
      const currentVal = anim.animations[0].currentValue;
      const numVal = typeof currentVal === 'number' ? currentVal : parseFloat(String(currentVal)) || 0;
      const value = numVal.toFixed(decimals);
      element.textContent = `${prefix}${value}${suffix}`;
    },
  });
}

/**
 * Progress bar animation
 */
export function progress(
  element: Element | null,
  percentage: number,
  options?: {
    duration?: number;
    easing?: string;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const { duration = DURATION.slow, easing = EASING.smooth } = options || {};

  return anime({
    targets: element,
    width: `${percentage}%`,
    duration,
    easing,
  });
}

/**
 * Spinner rotation
 */
export function spin(
  element: Element | null,
  options?: {
    duration?: number;
    loop?: boolean;
  }
): anime.AnimeInstance | null {
  if (!element) return null;

  const { duration = 1000, loop = true } = options || {};

  return anime({
    targets: element,
    rotate: 360,
    duration,
    easing: 'linear',
    loop,
  });
}

/**
 * Card hover lift effect
 */
export function cardHover(
  element: Element | null,
  isHovering: boolean
): anime.AnimeInstance | null {
  if (!element) return null;

  return anime({
    targets: element,
    translateY: isHovering ? -4 : 0,
    scale: isHovering ? 1.01 : 1,
    boxShadow: isHovering
      ? '0 10px 40px rgba(0, 0, 0, 0.12)'
      : '0 1px 3px rgba(0, 0, 0, 0.08)',
    duration: DURATION.fast,
    easing: EASING.smooth,
  });
}

/**
 * Cancel all animations on an element
 */
export function cancelAnimation(element: Element | Element[] | string | null): void {
  if (!element) return;
  anime.remove(element);
}

/**
 * React hook for anime.js animations
 */
export function useAnimeRef() {
  let animationRef: anime.AnimeInstance | null = null;

  const animate = (animation: anime.AnimeInstance | null) => {
    if (animationRef) {
      animationRef.pause();
    }
    animationRef = animation;
    return animationRef;
  };

  const cancel = () => {
    if (animationRef) {
      animationRef.pause();
      animationRef = null;
    }
  };

  return { animate, cancel };
}
