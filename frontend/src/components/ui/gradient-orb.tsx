'use client';

import { useRef } from 'react';
import { motion } from 'framer-motion';

interface GradientOrbProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'primary' | 'secondary' | 'accent';
  animated?: boolean;
  blur?: 'sm' | 'md' | 'lg' | 'xl';
}

const sizeMap = {
  sm: 'w-[300px] h-[300px]',
  md: 'w-[500px] h-[500px]',
  lg: 'w-[700px] h-[700px]',
  xl: 'w-[900px] h-[900px]',
};

const blurMap = {
  sm: 'blur-[40px]',
  md: 'blur-[60px]',
  lg: 'blur-[80px]',
  xl: 'blur-[100px]',
};

const colorMap = {
  primary: 'bg-primary/20',
  secondary: 'bg-blue-400/15',
  accent: 'bg-violet-400/15',
};

export function GradientOrb({
  className = '',
  size = 'lg',
  color = 'primary',
  animated = true,
  blur = 'lg',
}: GradientOrbProps) {
  const orbRef = useRef<HTMLDivElement>(null);

  return (
    <motion.div
      ref={orbRef}
      className={`
        absolute rounded-full pointer-events-none
        ${sizeMap[size]}
        ${blurMap[blur]}
        ${colorMap[color]}
        ${className}
      `}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={animated ? {
        opacity: 1,
        scale: [1, 1.05, 1],
        x: [0, 10, 0],
        y: [0, -10, 0],
      } : { opacity: 1, scale: 1 }}
      transition={animated ? {
        opacity: { duration: 0.8 },
        scale: {
          duration: 8,
          repeat: Infinity,
          ease: 'easeInOut',
        },
        x: {
          duration: 10,
          repeat: Infinity,
          ease: 'easeInOut',
        },
        y: {
          duration: 12,
          repeat: Infinity,
          ease: 'easeInOut',
        },
      } : { duration: 0.8 }}
    />
  );
}

// Multiple orbs composition for hero backgrounds
interface GradientBackgroundProps {
  className?: string;
  variant?: 'hero' | 'subtle' | 'vibrant';
}

export function GradientBackground({ 
  className = '',
  variant = 'hero',
}: GradientBackgroundProps) {
  if (variant === 'subtle') {
    return (
      <div className={`absolute inset-0 overflow-hidden -z-10 ${className}`}>
        <GradientOrb 
          size="lg" 
          color="primary" 
          blur="xl"
          className="top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-30"
        />
      </div>
    );
  }

  if (variant === 'vibrant') {
    return (
      <div className={`absolute inset-0 overflow-hidden -z-10 ${className}`}>
        <GradientOrb 
          size="xl" 
          color="primary" 
          blur="xl"
          className="top-0 left-1/4 -translate-x-1/2 -translate-y-1/4"
        />
        <GradientOrb 
          size="lg" 
          color="secondary" 
          blur="xl"
          className="bottom-0 right-1/4 translate-x-1/2 translate-y-1/4"
        />
        <GradientOrb 
          size="md" 
          color="accent" 
          blur="lg"
          className="top-1/2 right-0 translate-x-1/3"
        />
      </div>
    );
  }

  // Default: hero variant
  return (
    <div className={`absolute inset-0 overflow-hidden -z-10 ${className}`}>
      <GradientOrb 
        size="xl" 
        color="primary" 
        blur="xl"
        className="top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-40"
      />
      <GradientOrb 
        size="md" 
        color="secondary" 
        blur="lg"
        className="top-0 right-0 translate-x-1/3 -translate-y-1/3 opacity-30"
      />
    </div>
  );
}
