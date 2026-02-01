'use client';

import { useEffect, useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, InteractiveCard, HighlightedCard } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { RiskCard } from '@/components/risk-card';
import { ZoneSelector } from '@/components/zone-selector';
import { RiskBadge } from '@/components/risk-badge';
import { TrendIndicator } from '@/components/trend-indicator';
import { AnimatedCounter } from '@/components/ui/animated-counter';
import { useGSAP, gsap, prefersReducedMotion } from '@/lib/animations';
import { staggerContainerVariants, staggerItemVariants } from '@/lib/animations';
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
  const [selectedZone, setSelectedZone] = useState<string>('texas');
  const [risk, setRisk] = useState<RiskResponse | null>(null);
  const [history, setHistory] = useState<RiskHistoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDemo, setIsDemo] = useState(false);
  
  const metricsRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<HTMLDivElement>(null);

  // Fetch zones from API on mount
  useEffect(() => {
    async function fetchZones() {
      try {
        const response = await api.getZones();
        if (response.zones && response.zones.length > 0) {
          setZones(response.zones);
        }
      } catch (err) {
        console.warn('Failed to fetch zones, using demo data:', err);
      }
    }
    fetchZones();
  }, []);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError(null);
      
      try {
        const [riskData, historyData] = await Promise.all([
          api.getCurrentRisk(selectedZone),
          api.getRiskHistory(selectedZone, 30),
        ]);
        setRisk(riskData);
        setHistory(historyData);
        setIsDemo(false);
      } catch (err) {
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

  // GSAP animations for metrics cards
  useGSAP(() => {
    if (prefersReducedMotion() || loading) return;

    if (metricsRef.current) {
      gsap.fromTo(metricsRef.current.querySelectorAll('.metric-card'),
        { opacity: 0, y: 20, scale: 0.98 },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.5,
          stagger: 0.1,
          ease: 'power2.out',
        }
      );
    }

    if (chartRef.current) {
      gsap.fromTo(chartRef.current,
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          delay: 0.3,
          ease: 'power2.out',
        }
      );
    }
  }, { dependencies: [loading, risk] });

  const zoneName = zones.find(z => z.slug === selectedZone)?.name || selectedZone;

  // Prepare chart data
  const chartData = history?.snapshots.map((s, i) => ({
    day: i + 1,
    spi: s.spi_6m,
    date: new Date(s.created_at).toLocaleDateString(),
  })).reverse() || [];

  return (
    <div className="container py-8">
      {/* Header */}
      <motion.div 
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div>
          <span className="text-sm font-semibold text-primary mb-1 block tracking-wide uppercase">
            Risk Assessment
          </span>
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
      </motion.div>

      {/* Demo Mode Alert */}
      {isDemo && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Alert className="mb-6 bg-primary/5 border-primary/20">
            <Info className="h-4 w-4 text-primary" />
            <AlertTitle className="text-primary">Demo Mode</AlertTitle>
            <AlertDescription>
              Showing sample data. Connect to API for live risk assessments.
            </AlertDescription>
          </Alert>
        </motion.div>
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
            <Card key={i} className="animate-pulse">
              <CardHeader className="pb-2">
                <Skeleton className="h-4 w-24" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-10 w-20" />
                <Skeleton className="h-3 w-32 mt-2" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : risk ? (
        <>
          {/* Key Metrics Grid */}
          <div ref={metricsRef} className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
            {/* SPI Card */}
            <Card className="metric-card">
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2 text-sm font-medium">
                  <div className="p-1.5 rounded-lg bg-primary/10">
                    <Droplets className="h-4 w-4 text-primary" />
                  </div>
                  SPI-6 Index
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold tabular-nums text-foreground">
                  <AnimatedCounter value={risk.spi_6m} decimals={2} />
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                  Standardized Precipitation Index
                </p>
              </CardContent>
            </Card>

            {/* Risk Level Card */}
            <Card className="metric-card">
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2 text-sm font-medium">
                  <div className="p-1.5 rounded-lg bg-primary/10">
                    <BarChart3 className="h-4 w-4 text-primary" />
                  </div>
                  Risk Level
                </CardDescription>
              </CardHeader>
              <CardContent>
                <RiskBadge level={risk.risk_level} size="lg" pulse={risk.risk_level === 'CRITICAL'} />
                <p className="text-xs text-muted-foreground mt-3">
                  Based on SPI thresholds
                </p>
              </CardContent>
            </Card>

            {/* Days to Critical Card */}
            <HighlightedCard 
              className="metric-card"
              variant={risk.days_to_critical < 30 ? 'danger' : 'primary'}
            >
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2 text-sm font-medium">
                  <div className={`p-1.5 rounded-lg ${risk.days_to_critical < 30 ? 'bg-red-100' : 'bg-primary/10'}`}>
                    <Clock className={`h-4 w-4 ${risk.days_to_critical < 30 ? 'text-red-600' : 'text-primary'}`} />
                  </div>
                  Days to Critical
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className={`text-4xl font-bold tabular-nums ${
                  risk.days_to_critical < 30 
                    ? 'text-red-600' 
                    : 'text-foreground'
                }`}>
                  ~<AnimatedCounter value={risk.days_to_critical} />
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                  Estimated at current trend
                </p>
              </CardContent>
            </HighlightedCard>

            {/* Trend Card */}
            <Card className="metric-card">
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2 text-sm font-medium">
                  <div className="p-1.5 rounded-lg bg-primary/10">
                    <TrendingDown className="h-4 w-4 text-primary" />
                  </div>
                  Current Trend
                </CardDescription>
              </CardHeader>
              <CardContent>
                <TrendIndicator trend={risk.trend} size="lg" />
                <p className="text-xs text-muted-foreground mt-3">
                  Based on recent data
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Main Content Grid */}
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Risk Card - Main */}
            <motion.div 
              className="lg:col-span-1"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <RiskCard risk={risk} zoneName={zoneName} />
            </motion.div>

            {/* SPI History Chart */}
            <Card ref={chartRef} className="lg:col-span-2">
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
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                        <XAxis 
                          dataKey="day" 
                          tick={{ fontSize: 12, fill: 'var(--muted-foreground)' }}
                          tickLine={false}
                          axisLine={{ stroke: 'var(--border)' }}
                        />
                        <YAxis 
                          domain={[-3, 1]}
                          tick={{ fontSize: 12, fill: 'var(--muted-foreground)' }}
                          tickLine={false}
                          axisLine={{ stroke: 'var(--border)' }}
                        />
                        <Tooltip 
                          content={({ active, payload }) => {
                            if (active && payload && payload.length) {
                              return (
                                <div className="bg-background border border-border rounded-xl p-3 shadow-lg">
                                  <p className="text-sm font-semibold">
                                    SPI: {Number(payload[0].value).toFixed(2)}
                                  </p>
                                  <p className="text-xs text-muted-foreground mt-1">
                                    {payload[0].payload.date}
                                  </p>
                                </div>
                              );
                            }
                            return null;
                          }}
                        />
                        {/* Threshold lines */}
                        <ReferenceLine y={-2} stroke="#DF1B41" strokeDasharray="5 5" strokeWidth={1.5} />
                        <ReferenceLine y={-1.5} stroke="#ED5F00" strokeDasharray="5 5" strokeWidth={1.5} />
                        <ReferenceLine y={-1} stroke="#C4841D" strokeDasharray="5 5" strokeWidth={1.5} />
                        <Line
                          type="monotone"
                          dataKey="spi"
                          stroke="var(--primary)"
                          strokeWidth={2.5}
                          dot={false}
                          activeDot={{ r: 6, fill: 'var(--primary)', strokeWidth: 2, stroke: '#fff' }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <div className="h-[300px] flex items-center justify-center">
                    <div className="text-center">
                      <BarChart3 className="h-12 w-12 text-muted-foreground/30 mx-auto mb-3" />
                      <p className="text-muted-foreground">No historical data available in demo mode</p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Risk Interpretation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card className="mt-8">
              <CardHeader>
                <CardTitle>Risk Interpretation</CardTitle>
                <CardDescription>Understanding the SPI thresholds</CardDescription>
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
                      className={`p-4 rounded-xl border transition-all duration-200 ${
                        risk.risk_level === item.level 
                          ? 'ring-2 ring-primary border-primary/30 bg-primary/[0.02]' 
                          : 'border-border/60 hover:border-border'
                      }`}
                    >
                      <RiskBadge level={item.level} />
                      <p className="text-sm font-mono mt-3 text-foreground">SPI {item.spi}</p>
                      <p className="text-xs text-muted-foreground mt-1">{item.desc}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </>
      ) : null}
    </div>
  );
}
