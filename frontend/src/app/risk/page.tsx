'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { RiskCard } from '@/components/risk-card';
import { ZoneSelector } from '@/components/zone-selector';
import { RiskBadge } from '@/components/risk-badge';
import { TrendIndicator } from '@/components/trend-indicator';
import { 
  api, 
  DEMO_ZONES,
  type RiskResponse, 
  type Zone,
  type RiskHistoryResponse 
} from '@/lib/api';
import { 
  AlertCircle, 
  Info,
  Droplets,
  Clock,
  TrendingDown,
  BarChart3
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';

export default function RiskPage() {
  const [zones, setZones] = useState<Zone[]>(DEMO_ZONES);
  const [selectedZone, setSelectedZone] = useState<string>('cdmx');
  const [risk, setRisk] = useState<RiskResponse | null>(null);
  const [history, setHistory] = useState<RiskHistoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDemo, setIsDemo] = useState(false);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError(null);
      
      try {
        // Try to fetch from API
        const [riskData, historyData] = await Promise.all([
          api.getCurrentRisk(selectedZone),
          api.getRiskHistory(selectedZone, 30),
        ]);
        setRisk(riskData);
        setHistory(historyData);
        setIsDemo(false);
      } catch (err) {
        // Fallback to demo data
        console.warn('API unavailable, using demo data:', err);
        setRisk(api.getDemoRisk(selectedZone));
        setHistory(null);
        setIsDemo(true);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, [selectedZone]);

  const zoneName = zones.find(z => z.slug === selectedZone)?.name || selectedZone;

  // Prepare chart data
  const chartData = history?.snapshots.map((s, i) => ({
    day: i + 1,
    spi: s.spi_6m,
    date: new Date(s.created_at).toLocaleDateString(),
  })).reverse() || [];

  return (
    <div className="container py-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Risk Overview</h1>
          <p className="text-muted-foreground mt-1">
            Current drought risk assessment and historical trends
          </p>
        </div>
        <ZoneSelector 
          zones={zones} 
          value={selectedZone} 
          onChange={setSelectedZone} 
        />
      </div>

      {/* Demo Mode Alert */}
      {isDemo && (
        <Alert className="mb-6">
          <Info className="h-4 w-4" />
          <AlertTitle>Demo Mode</AlertTitle>
          <AlertDescription>
            Showing sample data. Connect to API for live risk assessments.
          </AlertDescription>
        </Alert>
      )}

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Loading State */}
      {loading ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-4 w-24" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-8 w-16" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : risk ? (
        <>
          {/* Key Metrics Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
            {/* SPI Card */}
            <Card>
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2">
                  <Droplets className="h-4 w-4" />
                  SPI-6 Index
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold tabular-nums">
                  {risk.spi_6m.toFixed(2)}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Standardized Precipitation Index
                </p>
              </CardContent>
            </Card>

            {/* Risk Level Card */}
            <Card>
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2">
                  <BarChart3 className="h-4 w-4" />
                  Risk Level
                </CardDescription>
              </CardHeader>
              <CardContent>
                <RiskBadge level={risk.risk_level} size="lg" pulse={risk.risk_level === 'CRITICAL'} />
                <p className="text-xs text-muted-foreground mt-2">
                  Based on SPI thresholds
                </p>
              </CardContent>
            </Card>

            {/* Days to Critical Card */}
            <Card className={risk.days_to_critical < 30 ? 'border-red-200 dark:border-red-900' : ''}>
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  Days to Critical
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className={`text-3xl font-bold tabular-nums ${
                  risk.days_to_critical < 30 ? 'text-red-600 dark:text-red-400' : ''
                }`}>
                  ~{risk.days_to_critical}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Estimated at current trend
                </p>
              </CardContent>
            </Card>

            {/* Trend Card */}
            <Card>
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2">
                  <TrendingDown className="h-4 w-4" />
                  Current Trend
                </CardDescription>
              </CardHeader>
              <CardContent>
                <TrendIndicator trend={risk.trend} size="lg" />
                <p className="text-xs text-muted-foreground mt-2">
                  Based on recent data
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Main Content Grid */}
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Risk Card - Main */}
            <div className="lg:col-span-1">
              <RiskCard risk={risk} zoneName={zoneName} />
            </div>

            {/* SPI History Chart */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>SPI-6 History</CardTitle>
                <CardDescription>
                  30-day historical trend for {zoneName}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {chartData.length > 0 ? (
                  <div className="h-[300px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                        <XAxis 
                          dataKey="day" 
                          tick={{ fontSize: 12 }}
                          tickLine={false}
                        />
                        <YAxis 
                          domain={[-3, 1]}
                          tick={{ fontSize: 12 }}
                          tickLine={false}
                        />
                        <Tooltip 
                          content={({ active, payload }) => {
                            if (active && payload && payload.length) {
                              return (
                                <div className="bg-background border rounded-lg p-3 shadow-lg">
                                  <p className="text-sm font-medium">
                                    SPI: {Number(payload[0].value).toFixed(2)}
                                  </p>
                                  <p className="text-xs text-muted-foreground">
                                    {payload[0].payload.date}
                                  </p>
                                </div>
                              );
                            }
                            return null;
                          }}
                        />
                        {/* Threshold lines */}
                        <ReferenceLine y={-2} stroke="#DC2626" strokeDasharray="5 5" label="Critical" />
                        <ReferenceLine y={-1.5} stroke="#EA580C" strokeDasharray="5 5" label="High" />
                        <ReferenceLine y={-1} stroke="#D97706" strokeDasharray="5 5" label="Medium" />
                        <Line
                          type="monotone"
                          dataKey="spi"
                          stroke="#2563EB"
                          strokeWidth={2}
                          dot={false}
                          activeDot={{ r: 6, fill: '#2563EB' }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                    <p>No historical data available in demo mode</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Risk Interpretation */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Risk Interpretation</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                  { level: 'LOW' as const, spi: '> -0.5', desc: 'Normal conditions' },
                  { level: 'MEDIUM' as const, spi: '-1.0 to -0.5', desc: 'Moderate drought' },
                  { level: 'HIGH' as const, spi: '-1.5 to -1.0', desc: 'Severe drought' },
                  { level: 'CRITICAL' as const, spi: '≤ -1.5', desc: 'Extreme drought' },
                ].map((item) => (
                  <div 
                    key={item.level}
                    className={`p-4 rounded-lg border ${
                      risk.risk_level === item.level ? 'ring-2 ring-primary' : ''
                    }`}
                  >
                    <RiskBadge level={item.level} />
                    <p className="text-sm font-mono mt-2">SPI {item.spi}</p>
                    <p className="text-xs text-muted-foreground">{item.desc}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </>
      ) : null}
    </div>
  );
}
