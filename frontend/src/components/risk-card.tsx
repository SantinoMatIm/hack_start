'use client';

import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle, HighlightedCard } from '@/components/ui/card';
import { RiskBadge } from './risk-badge';
import { TrendIndicator } from './trend-indicator';
import { AnimatedCounter } from '@/components/ui/animated-counter';
import type { RiskResponse } from '@/lib/api/types';
import { AlertTriangle, Clock, Droplets, Calendar } from 'lucide-react';

interface RiskCardProps {
  risk: RiskResponse;
  zoneName: string;
}

export function RiskCard({ risk, zoneName }: RiskCardProps) {
  const isUrgent = risk.days_to_critical < 30;
  
  const CardComponent = isUrgent ? HighlightedCard : Card;
  
  return (
    <CardComponent 
      variant={isUrgent ? 'danger' : undefined}
      className="relative overflow-hidden transition-all duration-300 h-full"
    >
      {/* Urgency indicator bar */}
      {isUrgent && (
        <motion.div 
          className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-red-500 to-orange-500"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.5 }}
        />
      )}
      
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">{zoneName}</CardTitle>
          <RiskBadge level={risk.risk_level} pulse={risk.risk_level === 'CRITICAL'} />
        </div>
      </CardHeader>
      
      <CardContent className="space-y-5">
        {/* SPI Value */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-muted-foreground">
            <div className="p-1.5 rounded-lg bg-primary/10">
              <Droplets className="h-4 w-4 text-primary" />
            </div>
            <span className="text-sm font-medium">SPI-6</span>
          </div>
          <span className="text-2xl font-bold tabular-nums">
            <AnimatedCounter value={risk.spi_6m} decimals={2} />
          </span>
        </div>
        
        {/* Days to Critical */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-muted-foreground">
            <div className={`p-1.5 rounded-lg ${isUrgent ? 'bg-red-100' : 'bg-primary/10'}`}>
              <Clock className={`h-4 w-4 ${isUrgent ? 'text-red-600' : 'text-primary'}`} />
            </div>
            <span className="text-sm font-medium">Days to Critical</span>
          </div>
          <div className="flex items-center gap-2">
            {isUrgent && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              >
                <AlertTriangle className="h-4 w-4 text-red-500" />
              </motion.div>
            )}
            <span className={`text-2xl font-bold tabular-nums ${isUrgent ? 'text-red-600' : ''}`}>
              ~<AnimatedCounter value={risk.days_to_critical} />
            </span>
          </div>
        </div>
        
        {/* Trend */}
        <div className="flex items-center justify-between pt-4 border-t">
          <span className="text-sm font-medium text-muted-foreground">Trend</span>
          <TrendIndicator trend={risk.trend} />
        </div>
        
        {/* Last Updated */}
        <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground pt-2">
          <Calendar className="h-3 w-3" />
          <span>Updated: {new Date(risk.last_updated).toLocaleDateString()}</span>
        </div>
      </CardContent>
    </CardComponent>
  );
}
