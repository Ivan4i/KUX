/**
 * Motion Components
 * Animated wrappers using Anime.js
 */

import React, { useEffect, useRef } from 'react';
import type { ReactNode } from 'react';
import anime from 'animejs';
import { motionPresets } from '../../hooks/useAnimeMotion';
import type { MotionPreset } from '../../hooks/useAnimeMotion';

interface MotionProps {
  children: ReactNode;
  preset?: MotionPreset;
  delay?: number;
  duration?: number;
  easing?: string;
  className?: string;
  style?: React.CSSProperties;
  onAnimationComplete?: () => void;
}

// Animated container that plays on mount
export const Motion: React.FC<MotionProps> = ({
  children,
  preset = 'fadeIn',
  delay = 0,
  duration,
  easing,
  className,
  style,
  onAnimationComplete,
}) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    const target = ref.current;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const presetConfig = motionPresets[preset];

    if (prefersReducedMotion) {
      // Reduced motion: instant show
      anime.set(target, { opacity: 1, scale: 1, translateX: 0, translateY: 0 });
      onAnimationComplete?.();
      return () => {
        anime.remove(target);
      };
    }

    anime({
      targets: target,
      ...presetConfig,
      duration: duration || presetConfig.duration,
      easing: easing || presetConfig.easing,
      delay,
      complete: onAnimationComplete,
    });

    return () => {
      anime.remove(target);
    };
  }, [preset, delay, duration, easing, onAnimationComplete]);

  return (
    <div ref={ref} className={className} style={{ ...style, opacity: 0 }}>
      {children}
    </div>
  );
};

// Fade in animation
export const FadeIn: React.FC<Omit<MotionProps, 'preset'>> = (props) => (
  <Motion {...props} preset="fadeIn" />
);

// Fade in from bottom
export const FadeInUp: React.FC<Omit<MotionProps, 'preset'>> = (props) => (
  <Motion {...props} preset="fadeInUp" />
);

// Fade in from top
export const FadeInDown: React.FC<Omit<MotionProps, 'preset'>> = (props) => (
  <Motion {...props} preset="fadeInDown" />
);

// Scale in animation
export const ScaleIn: React.FC<Omit<MotionProps, 'preset'>> = (props) => (
  <Motion {...props} preset="scaleIn" />
);

// Slide in from right
export const SlideInRight: React.FC<Omit<MotionProps, 'preset'>> = (props) => (
  <Motion {...props} preset="slideInRight" />
);

// Slide in from bottom (for bottom sheets)
export const SlideInUp: React.FC<Omit<MotionProps, 'preset'>> = (props) => (
  <Motion {...props} preset="slideInUp" />
);

// Staggered list animation
interface StaggerListProps {
  children: ReactNode[];
  preset?: MotionPreset;
  staggerDelay?: number;
  className?: string;
  itemClassName?: string;
}

export const StaggerList: React.FC<StaggerListProps> = ({
  children,
  preset = 'fadeInUp',
  staggerDelay = 50,
  className,
  itemClassName,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const items = containerRef.current.children;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const presetConfig = motionPresets[preset];

    if (prefersReducedMotion) {
      // Reduced motion: instant show all items
      anime.set(items, { opacity: 1, scale: 1, translateX: 0, translateY: 0 });
      return () => {
        anime.remove(items);
      };
    }

    anime({
      targets: items,
      ...presetConfig,
      delay: anime.stagger(staggerDelay),
    });

    return () => {
      anime.remove(items);
    };
  }, [preset, staggerDelay, children.length]);

  return (
    <div ref={containerRef} className={className}>
      {React.Children.map(children, (child, index) => (
        <div key={index} className={itemClassName} style={{ opacity: 0 }}>
          {child}
        </div>
      ))}
    </div>
  );
};

// Pulse animation (for notifications, badges)
interface PulseProps {
  children: ReactNode;
  active?: boolean;
  className?: string;
}

export const Pulse: React.FC<PulseProps> = ({ children, active = true, className }) => {
  const ref = useRef<HTMLDivElement>(null);
  const animationRef = useRef<anime.AnimeInstance | null>(null);

  useEffect(() => {
    if (!ref.current) return;

    const target = ref.current;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (active && !prefersReducedMotion) {
      animationRef.current = anime({
        targets: target,
        scale: [1, 1.1, 1],
        duration: 1000,
        easing: 'easeInOutQuad',
        loop: true,
      });
    } else if (active && prefersReducedMotion) {
      // Reduced motion: static state
      anime.set(target, { scale: 1 });
    } else {
      if (animationRef.current) {
        animationRef.current.pause();
        anime.remove(target);
      }
      anime.set(target, { scale: 1 });
    }

    return () => {
      if (animationRef.current) {
        animationRef.current.pause();
      }
      anime.remove(target);
      animationRef.current = null;
    };
  }, [active]);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
};

// Shake animation (for errors)
interface ShakeProps {
  children: ReactNode;
  trigger?: boolean;
  className?: string;
  onComplete?: () => void;
}

export const Shake: React.FC<ShakeProps> = ({ children, trigger, className, onComplete }) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current || !trigger) return;

    const target = ref.current;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion) {
      // Reduced motion: just call complete
      onComplete?.();
      return () => {
        anime.remove(target);
      };
    }

    anime({
      targets: target,
      translateX: [0, -10, 10, -10, 10, 0],
      duration: 500,
      easing: 'easeInOutQuad',
      complete: onComplete,
    });

    return () => {
      anime.remove(target);
    };
  }, [trigger, onComplete]);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
};

// Progress bar animation
interface AnimatedProgressProps {
  value: number;
  max?: number;
  duration?: number;
  className?: string;
  barClassName?: string;
}

export const AnimatedProgress: React.FC<AnimatedProgressProps> = ({
  value,
  max = 100,
  duration = 500,
  className,
  barClassName,
}) => {
  const barRef = useRef<HTMLDivElement>(null);
  const currentValue = useRef(0);

  useEffect(() => {
    if (!barRef.current) return;

    const target = barRef.current;
    const percentage = (value / max) * 100;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    anime({
      targets: target,
      width: `${percentage}%`,
      duration: prefersReducedMotion ? 0 : duration,
      easing: 'easeOutQuad',
      update: () => {
        currentValue.current = value;
      },
    });

    return () => {
      anime.remove(target);
    };
  }, [value, max, duration]);

  return (
    <div className={className} style={{ width: '100%', background: '#e5e7eb', borderRadius: 4 }}>
      <div
        ref={barRef}
        className={barClassName}
        style={{
          width: '0%',
          height: 4,
          background: 'var(--color-primary)',
          borderRadius: 4,
          transition: 'none',
        }}
      />
    </div>
  );
};

// Counter animation
interface AnimatedCounterProps {
  value: number;
  duration?: number;
  className?: string;
  formatFn?: (value: number) => string;
}

export const AnimatedCounter: React.FC<AnimatedCounterProps> = ({
  value,
  duration = 1000,
  className,
  formatFn = (v) => Math.round(v).toString(),
}) => {
  const ref = useRef<HTMLSpanElement>(null);
  const currentValue = useRef(0);
  const animationRef = useRef<anime.AnimeInstance | null>(null);

  useEffect(() => {
    if (!ref.current) return;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const obj = { value: currentValue.current };

    if (prefersReducedMotion) {
      // Reduced motion: instant update
      if (ref.current) {
        ref.current.textContent = formatFn(value);
      }
      currentValue.current = value;
      return;
    }

    animationRef.current = anime({
      targets: obj,
      value,
      duration,
      easing: 'easeOutQuad',
      round: 1,
      update: () => {
        if (ref.current) {
          ref.current.textContent = formatFn(obj.value);
        }
      },
      complete: () => {
        currentValue.current = value;
      },
    });

    return () => {
      if (animationRef.current) {
        animationRef.current.pause();
        animationRef.current = null;
      }
    };
  }, [value, duration, formatFn]);

  return (
    <span ref={ref} className={className}>
      {formatFn(currentValue.current)}
    </span>
  );
};

// Export all
export {
  Motion as default,
  type MotionProps,
  type StaggerListProps,
  type PulseProps,
  type ShakeProps,
  type AnimatedProgressProps,
  type AnimatedCounterProps,
};
