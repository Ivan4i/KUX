/**
 * Anime.js Motion System Hook
 * Provides reusable animations for UI elements
 *
 * Motion tokens aligned with V3-DESIGN_SYSTEM.md:
 * --duration-fast: 150ms
 * --duration-normal: 250ms
 * --duration-slow: 350ms
 * --ease-standard: cubic-bezier(0.16, 1, 0.3, 1)
 * --ease-entrance: cubic-bezier(0.34, 1.56, 0.64, 1)
 * --ease-exit: cubic-bezier(0.25, 0.46, 0.45, 0.94)
 */

import { useCallback, useRef } from 'react';
import anime from 'animejs';

// Motion duration constants (matching CSS tokens)
export const DURATION = {
  INSTANT: 0,
  FAST: 150,
  NORMAL: 250,
  SLOW: 350,
  SLOWER: 500,
} as const;

// Easing functions (matching CSS tokens)
export const EASING = {
  STANDARD: 'cubicBezier(0.16, 1, 0.3, 1)',
  ENTRANCE: 'cubicBezier(0.34, 1.56, 0.64, 1)',
  EXIT: 'cubicBezier(0.25, 0.46, 0.45, 0.94)',
  LINEAR: 'linear',
} as const;

// Animation presets (using motion token constants)
export const motionPresets = {
  // Entrance animations
  fadeIn: {
    opacity: [0, 1],
    duration: DURATION.NORMAL,
    easing: EASING.STANDARD,
  },
  fadeInUp: {
    opacity: [0, 1],
    translateY: [20, 0],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },
  fadeInDown: {
    opacity: [0, 1],
    translateY: [-20, 0],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },
  fadeInLeft: {
    opacity: [0, 1],
    translateX: [-20, 0],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },
  fadeInRight: {
    opacity: [0, 1],
    translateX: [20, 0],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },
  scaleIn: {
    opacity: [0, 1],
    scale: [0.9, 1],
    duration: DURATION.NORMAL,
    easing: EASING.ENTRANCE,
  },
  slideInRight: {
    translateX: ['100%', 0],
    opacity: [0, 1],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },
  slideInLeft: {
    translateX: ['-100%', 0],
    opacity: [0, 1],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },
  slideInUp: {
    translateY: ['100%', 0],
    opacity: [0, 1],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },
  slideInDown: {
    translateY: ['-100%', 0],
    opacity: [0, 1],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },

  // Exit animations
  fadeOut: {
    opacity: [1, 0],
    duration: DURATION.NORMAL,
    easing: EASING.EXIT,
  },
  fadeOutUp: {
    opacity: [1, 0],
    translateY: [0, -20],
    duration: DURATION.SLOW,
    easing: EASING.EXIT,
  },
  fadeOutDown: {
    opacity: [1, 0],
    translateY: [0, 20],
    duration: DURATION.SLOW,
    easing: EASING.EXIT,
  },
  scaleOut: {
    opacity: [1, 0],
    scale: [1, 0.9],
    duration: DURATION.NORMAL,
    easing: EASING.EXIT,
  },

  // Emphasis animations
  pulse: {
    scale: [1, 1.05, 1],
    duration: DURATION.SLOWER,
    easing: EASING.STANDARD,
  },
  shake: {
    translateX: [0, -10, 10, -10, 10, 0],
    duration: DURATION.SLOWER,
    easing: EASING.STANDARD,
  },
  bounce: {
    translateY: [0, -15, 0, -8, 0],
    duration: DURATION.SLOWER * 1.6,
    easing: EASING.STANDARD,
  },
  wiggle: {
    rotate: [0, -3, 3, -3, 3, 0],
    duration: DURATION.SLOWER,
    easing: EASING.STANDARD,
  },
  heartbeat: {
    scale: [1, 1.15, 1, 1.1, 1],
    duration: DURATION.SLOWER * 2,
    easing: EASING.STANDARD,
  },

  // Special animations (using teal color from V3)
  speaking: {
    boxShadow: [
      '0 0 0 0 rgba(33, 128, 137, 0.4)',
      '0 0 0 10px rgba(33, 128, 137, 0)',
      '0 0 0 0 rgba(33, 128, 137, 0.4)',
    ],
    duration: DURATION.SLOWER * 3,
    easing: EASING.STANDARD,
    loop: true,
  },
  recording: {
    opacity: [1, 0.5, 1],
    duration: DURATION.SLOWER * 2,
    easing: EASING.STANDARD,
    loop: true,
  },
  connecting: {
    rotate: 360,
    duration: DURATION.SLOWER * 2,
    easing: EASING.LINEAR,
    loop: true,
  },
};

export type MotionPreset = keyof typeof motionPresets;

interface UseAnimeMotionOptions {
  autoPlay?: boolean;
  delay?: number;
  loop?: boolean | number;
  onComplete?: () => void;
  onBegin?: () => void;
}

export function useAnimeMotion() {
  const animationRef = useRef<anime.AnimeInstance | null>(null);

  // Animate a single element with a preset
  const animate = useCallback(
    (
      target: HTMLElement | string | null,
      preset: MotionPreset | anime.AnimeParams,
      options: UseAnimeMotionOptions = {}
    ) => {
      if (!target) return null;

      const presetConfig = typeof preset === 'string' ? motionPresets[preset as MotionPreset] : preset;

      animationRef.current = anime({
        targets: target,
        ...presetConfig,
        autoplay: options.autoPlay !== false,
        delay: options.delay || 0,
        loop: options.loop ?? (presetConfig as any).loop ?? false,
        complete: options.onComplete,
        begin: options.onBegin,
      });

      return animationRef.current;
    },
    []
  );

  // Stagger animation for multiple elements
  const staggerAnimate = useCallback(
    (
      targets: HTMLElement[] | NodeListOf<Element> | string,
      preset: MotionPreset | anime.AnimeParams,
      staggerDelay: number = 50,
      options: UseAnimeMotionOptions = {}
    ) => {
      const presetConfig = typeof preset === 'string' ? motionPresets[preset as MotionPreset] : preset;

      animationRef.current = anime({
        targets,
        ...presetConfig,
        delay: anime.stagger(staggerDelay, { start: options.delay || 0 }),
        autoplay: options.autoPlay !== false,
        loop: options.loop ?? false,
        complete: options.onComplete,
        begin: options.onBegin,
      });

      return animationRef.current;
    },
    []
  );

  // Timeline for sequential animations
  const createTimeline = useCallback((options: anime.AnimeAnimParams = {}) => {
    return anime.timeline(options);
  }, []);

  // Pause current animation
  const pause = useCallback(() => {
    if (animationRef.current) {
      animationRef.current.pause();
    }
  }, []);

  // Play/resume current animation
  const play = useCallback(() => {
    if (animationRef.current) {
      animationRef.current.play();
    }
  }, []);

  // Restart animation
  const restart = useCallback(() => {
    if (animationRef.current) {
      animationRef.current.restart();
    }
  }, []);

  // Stop and remove animation
  const stop = useCallback(() => {
    if (animationRef.current) {
      anime.remove(animationRef.current);
      animationRef.current = null;
    }
  }, []);

  // Animate a value (for counters, progress, etc.)
  const animateValue = useCallback(
    (
      from: number,
      to: number,
      duration: number,
      onUpdate: (value: number) => void,
      easing: string = 'easeOutQuad'
    ) => {
      const obj = { value: from };

      return anime({
        targets: obj,
        value: to,
        duration,
        easing,
        round: 1,
        update: () => {
          onUpdate(obj.value);
        },
      });
    },
    []
  );

  return {
    animate,
    staggerAnimate,
    createTimeline,
    pause,
    play,
    restart,
    stop,
    animateValue,
    motionPresets,
  };
}

// Higher-level component animation helpers
export function animateOnMount(element: HTMLElement | null, preset: MotionPreset = 'fadeIn') {
  if (!element) return;

  anime({
    targets: element,
    ...motionPresets[preset],
    autoplay: true,
  });
}

export function animateOnUnmount(
  element: HTMLElement | null,
  preset: MotionPreset = 'fadeOut',
  onComplete?: () => void
) {
  if (!element) return;

  anime({
    targets: element,
    ...motionPresets[preset],
    autoplay: true,
    complete: onComplete,
  });
}

// Page transition animations (using motion tokens)
export const pageTransitions = {
  enter: {
    opacity: [0, 1],
    translateY: [20, 0],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },
  exit: {
    opacity: [1, 0],
    translateY: [0, -20],
    duration: DURATION.NORMAL,
    easing: EASING.EXIT,
  },
};

// Button interaction animations (using motion tokens)
export const buttonAnimations = {
  tap: {
    scale: [1, 0.95, 1],
    duration: DURATION.FAST,
    easing: EASING.STANDARD,
  },
  hover: {
    scale: [1, 1.02],
    duration: DURATION.FAST,
    easing: EASING.ENTRANCE,
  },
  success: {
    backgroundColor: ['#218089', '#218089'], // teal-500
    scale: [1, 1.05, 1],
    duration: DURATION.SLOW,
    easing: EASING.ENTRANCE,
  },
  error: {
    translateX: [0, -5, 5, -5, 5, 0],
    duration: DURATION.SLOW,
    easing: EASING.STANDARD,
  },
};

export default useAnimeMotion;
