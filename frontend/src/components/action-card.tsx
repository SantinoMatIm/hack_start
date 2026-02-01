'use client';

import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
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
    ? 'text-red-600 bg-red-50'
    : action.priority_score >= 60
    ? 'text-orange-600 bg-orange-50'
    : 'text-amber-600 bg-amber-50';

  return (
    <motion.div
      whileHover={{ y: -2 }}
      whileTap={{ scale: 0.995 }}
      transition={{ duration: 0.2 }}
    >
      <Card 
        className={cn(
          'relative transition-all duration-300 cursor-pointer h-full',
          'border-border/60 hover:shadow-lg hover:border-border',
          selected && 'ring-2 ring-primary border-primary/30 bg-primary/[0.02] shadow-[0_0_0_1px_rgba(99,91,255,0.1)]'
        )}
        onClick={() => onToggle?.(action.action_code)}
      >
        {/* Selection indicator */}
        <motion.div 
          className="absolute top-4 right-4"
          initial={false}
          animate={{ 
            scale: selected ? 1 : 0,
            opacity: selected ? 1 : 0 
          }}
          transition={{ duration: 0.2 }}
        >
          <div className="p-1 rounded-full bg-primary">
            <CheckCircle2 className="h-4 w-4 text-white" />
          </div>
        </motion.div>
        
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-4 pr-8">
            <div className="space-y-2">
              <CardTitle className="text-base font-semibold leading-tight">
                {action.title}
              </CardTitle>
              <Badge variant="outline" className="text-xs font-medium">
                {action.heuristic_id}
              </Badge>
            </div>
            <Badge className={cn('shrink-0 font-semibold', priorityColor)}>
              <Zap className="h-3 w-3 mr-1" />
              {action.priority_score}
            </Badge>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed">
            {action.description}
          </p>
          
          {/* Expected Effect */}
          <div className="flex items-center justify-between p-4 rounded-xl bg-emerald-50 border border-emerald-100">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-emerald-100">
                <Clock className="h-4 w-4 text-emerald-600" />
              </div>
              <span className="text-sm font-medium text-emerald-700">
                Days Gained
              </span>
            </div>
            <span className="text-xl font-bold text-emerald-600 tabular-nums">
              +{action.expected_effect.days_gained}
            </span>
          </div>
          
          {/* AI Method indicator */}
          {action.method === 'ai' && (
            <div className="flex items-center gap-2 text-xs text-primary font-medium">
              <Sparkles className="h-3.5 w-3.5" />
              <span>AI-parameterized</span>
            </div>
          )}
          
          {/* Justification */}
          <p className="text-xs text-muted-foreground italic line-clamp-2 leading-relaxed">
            &ldquo;{action.justification}&rdquo;
          </p>
        </CardContent>
      </Card>
    </motion.div>
  );
}
