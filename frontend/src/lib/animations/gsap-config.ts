'use client';

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';

// Register GSAP plugins
if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger, useGSAP);
}

// Default animation settings
export const GSAP_DEFAULTS = {
  duration: 0.8,
  ease: 'power3.out',
} as const;

// Stagger presets
export const STAGGER = {
  fast: 0.05,
  normal: 0.1,
  slow: 0.15,
} as const;

// Common animation configurations
export const animations = {
  // Fade up animation
  fadeUp: {
    from: { opacity: 0, y: 30 },
    to: { opacity: 1, y: 0, duration: GSAP_DEFAULTS.duration, ease: GSAP_DEFAULTS.ease },
  },
  
  // Fade in animation
  fadeIn: {
    from: { opacity: 0 },
    to: { opacity: 1, duration: 0.6, ease: 'power2.out' },
  },
  
  // Scale up animation
  scaleUp: {
    from: { opacity: 0, scale: 0.95 },
    to: { opacity: 1, scale: 1, duration: 0.5, ease: 'power2.out' },
  },
  
  // Slide in from left
  slideInLeft: {
    from: { opacity: 0, x: -50 },
    to: { opacity: 1, x: 0, duration: GSAP_DEFAULTS.duration, ease: GSAP_DEFAULTS.ease },
  },
  
  // Slide in from right
  slideInRight: {
    from: { opacity: 0, x: 50 },
    to: { opacity: 1, x: 0, duration: GSAP_DEFAULTS.duration, ease: GSAP_DEFAULTS.ease },
  },
  
  // Number counter animation helper
  counter: (target: HTMLElement, endValue: number, decimals: number = 0) => {
    const obj = { value: 0 };
    return gsap.to(obj, {
      value: endValue,
      duration: 1.5,
      ease: 'power2.out',
      onUpdate: () => {
        target.textContent = obj.value.toFixed(decimals);
      },
    });
  },
} as const;

// ScrollTrigger defaults
export const scrollTriggerDefaults = {
  start: 'top 85%',
  end: 'bottom 15%',
  toggleActions: 'play none none reverse',
} as const;

// Check for reduced motion preference
export const prefersReducedMotion = () => {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
};

// Safe animation wrapper that respects reduced motion
export const safeAnimate = (
  target: gsap.TweenTarget,
  vars: gsap.TweenVars
) => {
  if (prefersReducedMotion()) {
    // Skip animation, just set final state
    return gsap.set(target, { 
      opacity: vars.opacity ?? 1,
      x: 0,
      y: 0,
      scale: 1,
    });
  }
  return gsap.to(target, vars);
};

export { gsap, ScrollTrigger, useGSAP };
