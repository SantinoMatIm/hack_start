'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  Droplets, 
  BarChart3, 
  Zap, 
  Play, 
  ArrowRight,
  AlertTriangle,
  TrendingDown,
  Clock
} from 'lucide-react';

const features = [
  {
    icon: BarChart3,
    title: 'Risk Assessment',
    description: 'Real-time SPI-6 calculation with 4-level risk classification and trend analysis.',
    href: '/risk',
    color: 'text-blue-600 bg-blue-100 dark:bg-blue-950',
  },
  {
    icon: Zap,
    title: 'Smart Actions',
    description: 'AI-parameterized recommendations from 15 curated actions based on 6 heuristics.',
    href: '/actions',
    color: 'text-amber-600 bg-amber-100 dark:bg-amber-950',
  },
  {
    icon: Play,
    title: 'Scenario Simulation',
    description: 'Compare act vs. not-act outcomes with detailed trajectory projections.',
    href: '/simulation',
    color: 'text-emerald-600 bg-emerald-100 dark:bg-emerald-950',
  },
];

const stats = [
  { label: 'Pilot Zones', value: '2', sublabel: 'CDMX & Monterrey' },
  { label: 'Base Actions', value: '15', sublabel: 'Curated catalog' },
  { label: 'Heuristics', value: '6', sublabel: 'Decision rules' },
];

export default function HomePage() {
  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-primary/5 to-background border-b">
        <div className="container py-16 md:py-24">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium">
              <Droplets className="h-4 w-4" />
              Decision Intelligence Platform
            </div>
            
            {/* Headline */}
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight">
              Water Risk
              <span className="text-primary"> Management</span>
            </h1>
            
            {/* Subheadline */}
            <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
              Transform climate data into operational decisions. Prioritize actions, 
              simulate consequences, and manage drought risk with confidence.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Button asChild size="lg" className="gap-2">
                <Link href="/risk">
                  View Risk Status
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link href="/actions">
                  Explore Actions
                </Link>
              </Button>
            </div>
          </div>
        </div>
        
        {/* Background decoration */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/5 rounded-full blur-3xl" />
        </div>
      </section>
      
      {/* Stats Section */}
      <section className="border-b">
        <div className="container py-8">
          <div className="grid grid-cols-3 gap-8">
            {stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-primary">
                  {stat.value}
                </div>
                <div className="text-sm font-medium mt-1">{stat.label}</div>
                <div className="text-xs text-muted-foreground">{stat.sublabel}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Features Section */}
      <section className="container py-16">
        <div className="text-center mb-12">
          <h2 className="text-2xl md:text-3xl font-bold mb-3">
            Decision-First Platform
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Move beyond dashboards. Every feature is designed to help you decide faster, 
            with more clarity, and better understanding of consequences.
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Link key={feature.title} href={feature.href}>
                <Card className="h-full transition-all duration-200 hover:shadow-lg hover:-translate-y-1 cursor-pointer group">
                  <CardHeader>
                    <div className={`w-12 h-12 rounded-lg flex items-center justify-center mb-2 ${feature.color}`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <CardTitle className="flex items-center gap-2">
                      {feature.title}
                      <ArrowRight className="h-4 w-4 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                    </CardTitle>
                    <CardDescription>{feature.description}</CardDescription>
                  </CardHeader>
                </Card>
              </Link>
            );
          })}
        </div>
      </section>
      
      {/* Value Proposition */}
      <section className="border-t bg-muted/50">
        <div className="container py-16">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-2xl md:text-3xl font-bold text-center mb-8">
              Why This Platform?
            </h2>
            
            <div className="grid md:grid-cols-3 gap-6">
              <Card className="bg-background">
                <CardContent className="pt-6">
                  <AlertTriangle className="h-8 w-8 text-amber-600 mb-3" />
                  <h3 className="font-semibold mb-2">No More Dashboards</h3>
                  <p className="text-sm text-muted-foreground">
                    We don&apos;t just show data. We tell you what to do about it.
                  </p>
                </CardContent>
              </Card>
              
              <Card className="bg-background">
                <CardContent className="pt-6">
                  <TrendingDown className="h-8 w-8 text-red-600 mb-3" />
                  <h3 className="font-semibold mb-2">Cost of Inaction</h3>
                  <p className="text-sm text-muted-foreground">
                    See exactly what you lose by waiting. Consequences are visual.
                  </p>
                </CardContent>
              </Card>
              
              <Card className="bg-background">
                <CardContent className="pt-6">
                  <Clock className="h-8 w-8 text-blue-600 mb-3" />
                  <h3 className="font-semibold mb-2">Auditable AI</h3>
                  <p className="text-sm text-muted-foreground">
                    Every recommendation traces to numeric heuristics. No black boxes.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container text-center text-sm text-muted-foreground">
          <p>Water Risk Platform — Decision Intelligence for Drought Management</p>
          <p className="mt-1">Pilot Zones: Mexico City (CDMX) • Monterrey</p>
        </div>
      </footer>
    </div>
  );
}
