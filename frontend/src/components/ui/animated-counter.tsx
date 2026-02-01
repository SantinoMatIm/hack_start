'use client';

import { useEffect, useRef, useState } from 'react';
import { useGSAP, gsap, prefersReducedMotion } from '@/lib/animations';

interface AnimatedCounterProps {
  value: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  duration?: number;
  className?: string;
  delay?: number;
}

export function AnimatedCounter({
  value,
  decimals = 0,
  prefix = '',
  suffix = '',
  duration = 1.5,
  className = '',
  delay = 0,
}: AnimatedCounterProps) {
  const counterRef = useRef<HTMLSpanElement>(null);
  const [displayValue, setDisplayValue] = useState(0);
  const previousValue = useRef(0);

  useGSAP(() => {
    if (!counterRef.current) return;
    
    // Skip animation if reduced motion is preferred
    if (prefersReducedMotion()) {
      setDisplayValue(value);
      return;
    }

    const obj = { value: previousValue.current };
    
    gsap.to(obj, {
      value: value,
      duration: duration,
      delay: delay,
      ease: 'power2.out',
      onUpdate: () => {
        setDisplayValue(obj.value);
      },
      onComplete: () => {
        previousValue.current = value;
      },
    });
  }, [value, duration, delay]);

  const formattedValue = displayValue.toFixed(decimals);

  return (
    <span ref={counterRef} className={`tabular-nums ${className}`}>
      {prefix}{formattedValue}{suffix}
    </span>
  );
}

// Simpler version for basic number animations
interface SimpleCounterProps {
  end: number;
  className?: string;
}

export function SimpleCounter({ end, className = '' }: SimpleCounterProps) {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    if (prefersReducedMotion()) {
      setCount(end);
      return;
    }

    let startTime: number;
    const duration = 1500;
    
    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / duration, 1);
      
      // Easing function (ease-out)
      const easeOut = 1 - Math.pow(1 - progress, 3);
      
      setCount(Math.floor(easeOut * end));
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  }, [end]);

  return <span className={`tabular-nums ${className}`}>{count}</span>;
}
