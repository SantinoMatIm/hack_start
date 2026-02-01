'use client';

import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import type { Trend } from '@/lib/api/types';
import { cn } from '@/lib/utils';

interface TrendIndicatorProps {
  trend: Trend;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

const trendConfig: Record<Trend, { 
  label: string; 
  icon: typeof TrendingUp; 
  className: string;
}> = {
  IMPROVING: {
    label: 'Improving',
    icon: TrendingUp,
    className: 'text-emerald-600 dark:text-emerald-400',
  },
  STABLE: {
    label: 'Stable',
    icon: Minus,
    className: 'text-slate-500 dark:text-slate-400',
  },
  WORSENING: {
    label: 'Worsening',
    icon: TrendingDown,
    className: 'text-red-600 dark:text-red-400',
  },
};

const sizeClasses = {
  sm: { icon: 14, text: 'text-xs' },
  md: { icon: 18, text: 'text-sm' },
  lg: { icon: 22, text: 'text-base' },
};

export function TrendIndicator({ trend, showLabel = true, size = 'md' }: TrendIndicatorProps) {
  const config = trendConfig[trend];
  const Icon = config.icon;
  const sizeConfig = sizeClasses[size];
  
  return (
    <div className={cn('flex items-center gap-1.5', config.className)}>
      <Icon size={sizeConfig.icon} />
      {showLabel && (
        <span className={cn('font-medium', sizeConfig.text)}>
          {config.label}
        </span>
      )}
    </div>
  );
}
