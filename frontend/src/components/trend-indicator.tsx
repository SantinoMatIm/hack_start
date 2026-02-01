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
  bgClassName: string;
}> = {
  IMPROVING: {
    label: 'Improving',
    icon: TrendingUp,
    className: 'text-emerald-600',
    bgClassName: 'bg-emerald-100',
  },
  STABLE: {
    label: 'Stable',
    icon: Minus,
    className: 'text-slate-600',
    bgClassName: 'bg-slate-100',
  },
  WORSENING: {
    label: 'Worsening',
    icon: TrendingDown,
    className: 'text-red-600',
    bgClassName: 'bg-red-100',
  },
};

const sizeClasses = {
  sm: { icon: 14, text: 'text-xs', padding: 'p-1' },
  md: { icon: 18, text: 'text-sm', padding: 'p-1.5' },
  lg: { icon: 22, text: 'text-base', padding: 'p-2' },
};

export function TrendIndicator({ trend, showLabel = true, size = 'md' }: TrendIndicatorProps) {
  const config = trendConfig[trend];
  const Icon = config.icon;
  const sizeConfig = sizeClasses[size];
  
  return (
    <div className={cn('flex items-center gap-2', config.className)}>
      <div className={cn('rounded-lg', config.bgClassName, sizeConfig.padding)}>
        <Icon size={sizeConfig.icon} />
      </div>
      {showLabel && (
        <span className={cn('font-semibold', sizeConfig.text)}>
          {config.label}
        </span>
      )}
    </div>
  );
}
