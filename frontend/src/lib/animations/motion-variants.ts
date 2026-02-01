import { Variants, Transition } from 'framer-motion';

// Default transition
export const defaultTransition: Transition = {
  duration: 0.3,
  ease: [0.25, 0.1, 0.25, 1], // Custom cubic-bezier for smooth feel
};

// Spring transition for bouncy effects
export const springTransition: Transition = {
  type: 'spring',
  stiffness: 300,
  damping: 30,
};

// Page transition variants
export const pageVariants: Variants = {
  initial: {
    opacity: 0,
    y: 8,
  },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
  exit: {
    opacity: 0,
    y: -8,
    transition: {
      duration: 0.3,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
};

// Fade variants
export const fadeVariants: Variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.4 } },
  exit: { opacity: 0, transition: { duration: 0.3 } },
};

// Fade up variants
export const fadeUpVariants: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: { 
    opacity: 1, 
    y: 0,
    transition: {
      duration: 0.5,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
  exit: { 
    opacity: 0, 
    y: -10,
    transition: { duration: 0.3 },
  },
};

// Scale variants (for cards, buttons)
export const scaleVariants: Variants = {
  initial: { opacity: 0, scale: 0.96 },
  animate: { 
    opacity: 1, 
    scale: 1,
    transition: {
      duration: 0.4,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
  exit: { 
    opacity: 0, 
    scale: 0.96,
    transition: { duration: 0.3 },
  },
};

// Stagger container variants
export const staggerContainerVariants: Variants = {
  initial: {},
  animate: {
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

// Stagger item variants
export const staggerItemVariants: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: { 
    opacity: 1, 
    y: 0,
    transition: {
      duration: 0.5,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
};

// Card hover variants
export const cardHoverVariants: Variants = {
  initial: { y: 0, boxShadow: '0 1px 3px rgba(0,0,0,0.08)' },
  hover: { 
    y: -4, 
    boxShadow: '0 12px 40px rgba(0,0,0,0.12)',
    transition: {
      duration: 0.3,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
  tap: { 
    y: -2, 
    scale: 0.99,
    transition: { duration: 0.1 },
  },
};

// Button hover variants
export const buttonHoverVariants: Variants = {
  initial: { scale: 1 },
  hover: { 
    scale: 1.02,
    transition: { duration: 0.2, ease: 'easeOut' },
  },
  tap: { 
    scale: 0.98,
    transition: { duration: 0.1 },
  },
};

// Slide variants (for drawers, panels)
export const slideInRightVariants: Variants = {
  initial: { x: '100%', opacity: 0 },
  animate: { 
    x: 0, 
    opacity: 1,
    transition: {
      duration: 0.4,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
  exit: { 
    x: '100%', 
    opacity: 0,
    transition: {
      duration: 0.3,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
};

// Slide up variants (for modals, bottom sheets)
export const slideUpVariants: Variants = {
  initial: { y: '100%', opacity: 0 },
  animate: { 
    y: 0, 
    opacity: 1,
    transition: {
      duration: 0.4,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
  exit: { 
    y: '100%', 
    opacity: 0,
    transition: {
      duration: 0.3,
      ease: [0.25, 0.1, 0.25, 1],
    },
  },
};

// Backdrop variants
export const backdropVariants: Variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.3 } },
  exit: { opacity: 0, transition: { duration: 0.2 } },
};

// Pulse animation for urgent elements
export const pulseVariants: Variants = {
  initial: { scale: 1, opacity: 1 },
  animate: {
    scale: [1, 1.05, 1],
    opacity: [1, 0.8, 1],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
};

// Number counter animation (use with motion.span and animate prop)
export const counterVariants = (value: number): Variants => ({
  initial: { opacity: 0 },
  animate: { 
    opacity: 1,
    transition: { duration: 0.3 },
  },
});

// Reduced motion variants (instant transitions)
export const reducedMotionVariants: Variants = {
  initial: { opacity: 1 },
  animate: { opacity: 1 },
  exit: { opacity: 1 },
};
