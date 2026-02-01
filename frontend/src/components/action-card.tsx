'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import type { RecommendedAction } from '@/lib/api/types';
import { CheckCircle2, Clock, Sparkles, Zap } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ActionCardProps {
  action: RecommendedAction;
  selected?: boolean;
  onToggle?: (code: string) => void;
}

export function ActionCard({ action, selected = false, onToggle }: ActionCardProps) {
  const priorityColor = action.priority_score >= 80 
    ? 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-950'
    : action.priority_score >= 60
    ? 'text-orange-600 bg-orange-50 dark:text-orange-400 dark:bg-orange-950'
    : 'text-amber-600 bg-amber-50 dark:text-amber-400 dark:bg-amber-950';

  return (
    <Card className={cn(
      'relative transition-all duration-200 cursor-pointer hover:shadow-md',
      selected && 'ring-2 ring-primary border-primary'
    )}
    onClick={() => onToggle?.(action.action_code)}
    >
      {/* Selection indicator */}
      {selected && (
        <div className="absolute top-3 right-3">
          <CheckCircle2 className="h-5 w-5 text-primary" />
        </div>
      )}
      
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-1">
            <CardTitle className="text-base font-semibold leading-tight">
              {action.title}
            </CardTitle>
            <Badge variant="outline" className="text-xs">
              {action.heuristic_id}
            </Badge>
          </div>
          <Badge className={cn('shrink-0', priorityColor)}>
            <Zap className="h-3 w-3 mr-1" />
            {action.priority_score}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-3">
        <p className="text-sm text-muted-foreground line-clamp-2">
          {action.description}
        </p>
        
        {/* Expected Effect */}
        <div className="flex items-center justify-between p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-100 dark:border-emerald-900">
          <div className="flex items-center gap-2">
            <Clock className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
            <span className="text-sm font-medium text-emerald-700 dark:text-emerald-300">
              Days Gained
            </span>
          </div>
          <span className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
            +{action.expected_effect.days_gained}
          </span>
        </div>
        
        {/* AI Method indicator */}
        {action.method === 'ai' && (
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Sparkles className="h-3 w-3" />
            <span>AI-parameterized</span>
          </div>
        )}
        
        {/* Justification */}
        <p className="text-xs text-muted-foreground italic line-clamp-2">
          &ldquo;{action.justification}&rdquo;
        </p>
      </CardContent>
    </Card>
  );
}
