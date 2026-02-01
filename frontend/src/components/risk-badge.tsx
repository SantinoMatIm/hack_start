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
    className: 'bg-red-100 text-red-700 border-red-200',
  },
  HIGH: {
    label: 'High',
    className: 'bg-orange-100 text-orange-700 border-orange-200',
  },
  MEDIUM: {
    label: 'Medium',
    className: 'bg-amber-100 text-amber-700 border-amber-200',
  },
  LOW: {
    label: 'Low',
    className: 'bg-emerald-100 text-emerald-700 border-emerald-200',
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
        'font-medium',
        pulse && level === 'CRITICAL' && 'animate-pulse-subtle'
      )}
    >
      {config.label}
    </Badge>
  );
}
