'use client';

import { Badge } from '@/components/ui/badge';
import type { RiskLevel } from '@/lib/api/types';
import { cn } from '@/lib/utils';

interface RiskBadgeProps {
  level: RiskLevel;
  size?: 'sm' | 'md' | 'lg';
  pulse?: boolean;
}

const riskConfig: Record<RiskLevel, { label: string; className: string }> = {
  CRITICAL: {
    label: 'Critical',
    className: 'bg-red-100 text-red-700 border-red-200 dark:bg-red-950 dark:text-red-400 dark:border-red-900',
  },
  HIGH: {
    label: 'High',
    className: 'bg-orange-100 text-orange-700 border-orange-200 dark:bg-orange-950 dark:text-orange-400 dark:border-orange-900',
  },
  MEDIUM: {
    label: 'Medium',
    className: 'bg-amber-100 text-amber-700 border-amber-200 dark:bg-amber-950 dark:text-amber-400 dark:border-amber-900',
  },
  LOW: {
    label: 'Low',
    className: 'bg-emerald-100 text-emerald-700 border-emerald-200 dark:bg-emerald-950 dark:text-emerald-400 dark:border-emerald-900',
  },
};

const sizeClasses = {
  sm: 'text-xs px-2 py-0.5',
  md: 'text-sm px-2.5 py-1',
  lg: 'text-base px-3 py-1.5 font-semibold',
};

export function RiskBadge({ level, size = 'md', pulse = false }: RiskBadgeProps) {
  const config = riskConfig[level];
  
  return (
    <Badge
      variant="outline"
      className={cn(
        config.className,
        sizeClasses[size],
        pulse && level === 'CRITICAL' && 'animate-pulse-risk'
      )}
    >
      {config.label}
    </Badge>
  );
}
