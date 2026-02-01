'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { RiskBadge } from './risk-badge';
import { TrendIndicator } from './trend-indicator';
import type { RiskResponse } from '@/lib/api/types';
import { AlertTriangle, Clock, Droplets } from 'lucide-react';

interface RiskCardProps {
  risk: RiskResponse;
  zoneName: string;
}

export function RiskCard({ risk, zoneName }: RiskCardProps) {
  const isUrgent = risk.days_to_critical < 30;
  
  return (
    <Card className={`
      relative overflow-hidden transition-all duration-300
      ${isUrgent ? 'border-red-200 dark:border-red-900' : ''}
    `}>
      {/* Urgency indicator bar */}
      {isUrgent && (
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-red-500 to-orange-500" />
      )}
      
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">{zoneName}</CardTitle>
          <RiskBadge level={risk.risk_level} pulse={risk.risk_level === 'CRITICAL'} />
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* SPI Value */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Droplets className="h-4 w-4" />
            <span className="text-sm">SPI-6</span>
          </div>
          <span className="text-2xl font-bold tabular-nums">
            {risk.spi_6m.toFixed(2)}
          </span>
        </div>
        
        {/* Days to Critical */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Clock className="h-4 w-4" />
            <span className="text-sm">Days to Critical</span>
          </div>
          <div className="flex items-center gap-2">
            {isUrgent && <AlertTriangle className="h-4 w-4 text-red-500" />}
            <span className={`text-2xl font-bold tabular-nums ${isUrgent ? 'text-red-600 dark:text-red-400' : ''}`}>
              ~{risk.days_to_critical}
            </span>
          </div>
        </div>
        
        {/* Trend */}
        <div className="flex items-center justify-between pt-2 border-t">
          <span className="text-sm text-muted-foreground">Trend</span>
          <TrendIndicator trend={risk.trend} />
        </div>
        
        {/* Estimated label */}
        <p className="text-xs text-muted-foreground text-center">
          Last updated: {new Date(risk.last_updated).toLocaleDateString()}
        </p>
      </CardContent>
    </Card>
  );
}
