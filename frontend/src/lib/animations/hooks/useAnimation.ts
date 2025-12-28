/**
 * useAnimation Hook
 * React hook for managing anime.js animations with proper cleanup
 */

import { useRef, useEffect, useCallback } from 'react';
import anime from 'animejs';
import * as animations from '../utils/animations';

/**
 * Hook for managing a single animation instance
 */
export function useAnimation() {
  const animationRef = useRef<anime.AnimeInstance | null>(null);
  const targetRef = useRef<HTMLElement | null>(null);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (animationRef.current) {
        animationRef.current.pause();
        animationRef.current = null;
      }
    };
  }, []);

  const animate = useCallback((animation: anime.AnimeInstance | null) => {
    // Cancel previous animation
    if (animationRef.current) {
      animationRef.current.pause();
    }
    animationRef.current = animation;
    return animation;
  }, []);

  const cancel = useCallback(() => {
    if (animationRef.current) {
      animationRef.current.pause();
      animationRef.current = null;
    }
  }, []);

  const setTarget = useCallback((element: HTMLElement | null) => {
    targetRef.current = element;
  }, []);

  return {
    animate,
    cancel,
    setTarget,
    targetRef,
    animationRef,
  };
}

/**
 * Hook for entrance animations
 */
export function useEntranceAnimation(
  type: 'fadeIn' | 'scaleIn' | 'slideIn' = 'fadeIn',
  options?: {
    delay?: number;
    duration?: number;
    direction?: 'left' | 'right' | 'up' | 'down';
    disabled?: boolean;
  }
) {
  const ref = useRef<HTMLElement | null>(null);
  const hasAnimated = useRef(false);

  useEffect(() => {
    if (!ref.current || hasAnimated.current || options?.disabled) return;

    const element = ref.current;

    // Set initial state
    element.style.opacity = '0';

    // Small delay to ensure element is in DOM
    requestAnimationFrame(() => {
      hasAnimated.current = true;

      switch (type) {
        case 'fadeIn':
          animations.fadeIn(element, {
            delay: options?.delay,
            duration: options?.duration,
          });
          break;
        case 'scaleIn':
          animations.scaleIn(element, {
            delay: options?.delay,
            duration: options?.duration,
          });
          break;
        case 'slideIn':
          animations.slideIn(element, options?.direction || 'up', {
            delay: options?.delay,
            duration: options?.duration,
          });
          break;
      }
    });
  }, [type, options?.delay, options?.duration, options?.direction, options?.disabled]);

  return ref;
}

/**
 * Hook for staggered list animations
 */
export function useStaggerAnimation<T>(
  items: T[],
  options?: {
    staggerDelay?: number;
    duration?: number;
    selector?: string;
  }
) {
  const containerRef = useRef<HTMLElement | null>(null);
  const prevLengthRef = useRef(0);

  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const selector = options?.selector || '> *';
    const elements = container.querySelectorAll(selector);

    // Only animate new items
    if (items.length > prevLengthRef.current) {
      const newElements = Array.from(elements).slice(prevLengthRef.current);

      if (newElements.length > 0) {
        animations.staggerIn(newElements, {
          staggerDelay: options?.staggerDelay,
          duration: options?.duration,
        });
      }
    }

    prevLengthRef.current = items.length;
  }, [items.length, options?.staggerDelay, options?.duration, options?.selector]);

  return containerRef;
}

/**
 * Hook for hover animations
 */
export function useHoverAnimation(
  type: 'lift' | 'scale' | 'pulse' = 'lift'
) {
  const ref = useRef<HTMLElement | null>(null);
  const animationRef = useRef<anime.AnimeInstance | null>(null);

  const handleMouseEnter = useCallback(() => {
    if (!ref.current) return;

    if (animationRef.current) {
      animationRef.current.pause();
    }

    switch (type) {
      case 'lift':
        animationRef.current = animations.cardHover(ref.current, true);
        break;
      case 'scale':
        animationRef.current = anime({
          targets: ref.current,
          scale: 1.02,
          duration: animations.DURATION.fast,
          easing: animations.EASING.smooth,
        });
        break;
      case 'pulse':
        animationRef.current = animations.pulse(ref.current, { loop: true });
        break;
    }
  }, [type]);

  const handleMouseLeave = useCallback(() => {
    if (!ref.current) return;

    if (animationRef.current) {
      animationRef.current.pause();
    }

    switch (type) {
      case 'lift':
        animationRef.current = animations.cardHover(ref.current, false);
        break;
      case 'scale':
        animationRef.current = anime({
          targets: ref.current,
          scale: 1,
          duration: animations.DURATION.fast,
          easing: animations.EASING.smooth,
        });
        break;
      case 'pulse':
        animationRef.current = anime({
          targets: ref.current,
          scale: 1,
          duration: animations.DURATION.fast,
          easing: animations.EASING.smooth,
        });
        break;
    }
  }, [type]);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    element.addEventListener('mouseenter', handleMouseEnter);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mouseenter', handleMouseEnter);
      element.removeEventListener('mouseleave', handleMouseLeave);
      if (animationRef.current) {
        animationRef.current.pause();
      }
    };
  }, [handleMouseEnter, handleMouseLeave]);

  return ref;
}

/**
 * Hook for button press animation
 */
export function useButtonPress() {
  const ref = useRef<HTMLElement | null>(null);

  const handlePress = useCallback(() => {
    if (ref.current) {
      animations.buttonPress(ref.current);
    }
  }, []);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    element.addEventListener('mousedown', handlePress);

    return () => {
      element.removeEventListener('mousedown', handlePress);
    };
  }, [handlePress]);

  return ref;
}

/**
 * Hook for counting animation
 */
export function useCountUp(
  endValue: number,
  options?: {
    startValue?: number;
    duration?: number;
    decimals?: number;
    prefix?: string;
    suffix?: string;
    autoStart?: boolean;
  }
) {
  const ref = useRef<HTMLElement | null>(null);
  const animationRef = useRef<anime.AnimeInstance | null>(null);

  const start = useCallback(() => {
    if (ref.current) {
      animationRef.current = animations.countUp(ref.current, endValue, options);
    }
  }, [endValue, options]);

  const reset = useCallback(() => {
    if (animationRef.current) {
      animationRef.current.pause();
    }
    if (ref.current) {
      ref.current.textContent = `${options?.prefix || ''}${options?.startValue || 0}${options?.suffix || ''}`;
    }
  }, [options]);

  useEffect(() => {
    if (options?.autoStart !== false) {
      start();
    }
    return () => {
      if (animationRef.current) {
        animationRef.current.pause();
      }
    };
  }, [start, options?.autoStart]);

  return { ref, start, reset };
}

export default useAnimation;
