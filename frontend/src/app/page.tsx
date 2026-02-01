'use client';

import { useRef } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, InteractiveCard } from '@/components/ui/card';
import { GradientBackground } from '@/components/ui/gradient-orb';
import { useGSAP, gsap, ScrollTrigger, prefersReducedMotion } from '@/lib/animations';
import { 
  staggerContainerVariants, 
  staggerItemVariants,
  fadeUpVariants,
} from '@/lib/animations';
import { 
  Droplets, 
  BarChart3, 
  Zap, 
  Play, 
  ArrowRight,
  AlertTriangle,
  TrendingDown,
  Clock,
  Shield,
  LineChart,
  Target
} from 'lucide-react';

const features = [
  {
    icon: BarChart3,
    title: 'Risk Assessment',
    description: 'Real-time SPI-6 calculation with 4-level risk classification and trend analysis.',
    href: '/risk',
  },
  {
    icon: Zap,
    title: 'Smart Actions',
    description: 'AI-parameterized recommendations from 15 curated actions based on 6 heuristics.',
    href: '/actions',
  },
  {
    icon: Play,
    title: 'Scenario Simulation',
    description: 'Compare act vs. not-act outcomes with detailed trajectory projections.',
    href: '/simulation',
  },
];

const stats = [
  { label: 'Pilot Zones', value: '2', sublabel: 'CDMX & Monterrey' },
  { label: 'Base Actions', value: '15', sublabel: 'Curated catalog' },
  { label: 'Heuristics', value: '6', sublabel: 'Decision rules' },
];

const valueProps = [
  {
    icon: AlertTriangle,
    title: 'No More Dashboards',
    description: "We don't just show data. We tell you what to do about it.",
    color: 'text-amber-600',
  },
  {
    icon: TrendingDown,
    title: 'Cost of Inaction',
    description: 'See exactly what you lose by waiting. Consequences are visual.',
    color: 'text-red-500',
  },
  {
    icon: Clock,
    title: 'Auditable AI',
    description: 'Every recommendation traces to numeric heuristics. No black boxes.',
    color: 'text-primary',
  },
];

export default function HomePage() {
  const heroRef = useRef<HTMLDivElement>(null);
  const featuresRef = useRef<HTMLDivElement>(null);
  const statsRef = useRef<HTMLDivElement>(null);
  const valueRef = useRef<HTMLDivElement>(null);

  // GSAP animations
  useGSAP(() => {
    if (prefersReducedMotion()) return;

    // Hero text reveal
    const heroTl = gsap.timeline({ defaults: { ease: 'power3.out' } });
    
    heroTl
      .fromTo('.hero-badge', 
        { opacity: 0, y: 20, scale: 0.9 },
        { opacity: 1, y: 0, scale: 1, duration: 0.6 }
      )
      .fromTo('.hero-title', 
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.8 },
        '-=0.3'
      )
      .fromTo('.hero-subtitle', 
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.6 },
        '-=0.4'
      )
      .fromTo('.hero-cta', 
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.5, stagger: 0.1 },
        '-=0.3'
      );

    // Stats counter animation on scroll
    if (statsRef.current) {
      gsap.fromTo(statsRef.current.querySelectorAll('.stat-item'),
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          stagger: 0.1,
          scrollTrigger: {
            trigger: statsRef.current,
            start: 'top 85%',
          },
        }
      );
    }

    // Features cards scroll reveal
    if (featuresRef.current) {
      gsap.fromTo(featuresRef.current.querySelectorAll('.feature-card'),
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 0.7,
          stagger: 0.15,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: featuresRef.current,
            start: 'top 80%',
          },
        }
      );
    }

    // Value props scroll reveal
    if (valueRef.current) {
      gsap.fromTo(valueRef.current.querySelectorAll('.value-card'),
        { opacity: 0, y: 30, scale: 0.95 },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.6,
          stagger: 0.12,
          scrollTrigger: {
            trigger: valueRef.current,
            start: 'top 80%',
          },
        }
      );
    }
  }, { scope: heroRef });

  return (
    <div ref={heroRef}>
      {/* Hero Section */}
      <section className="relative overflow-hidden border-b">
        {/* Gradient Background */}
        <GradientBackground variant="hero" />
        
        <div className="container py-20 md:py-32">
          <div className="max-w-3xl mx-auto text-center space-y-8">
            {/* Badge */}
            <motion.div 
              className="hero-badge inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium border border-primary/20"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <Droplets className="h-4 w-4" />
              Decision Intelligence Platform
            </motion.div>
            
            {/* Headline */}
            <h1 className="hero-title text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight text-foreground">
              Water Risk
              <span className="text-gradient"> Management</span>
            </h1>
            
            {/* Subheadline */}
            <p className="hero-subtitle text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Transform climate data into operational decisions. Prioritize actions, 
              simulate consequences, and manage drought risk with confidence.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Button asChild size="lg" className="hero-cta gap-2 shadow-lg shadow-primary/25">
                <Link href="/risk">
                  View Risk Status
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="hero-cta">
                <Link href="/actions">
                  Explore Actions
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
      
      {/* Stats Section */}
      <section ref={statsRef} className="border-b bg-secondary/30">
        <div className="container py-12">
          <div className="grid grid-cols-3 gap-8 md:gap-12">
            {stats.map((stat) => (
              <div key={stat.label} className="stat-item text-center">
                <div className="text-3xl md:text-4xl lg:text-5xl font-bold text-primary tabular-nums">
                  {stat.value}
                </div>
                <div className="text-sm md:text-base font-semibold mt-2 text-foreground">{stat.label}</div>
                <div className="text-xs md:text-sm text-muted-foreground mt-1">{stat.sublabel}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Features Section */}
      <section className="container py-20 md:py-28">
        <div className="text-center mb-16">
          <motion.span 
            className="inline-block text-sm font-semibold text-primary mb-3 tracking-wide uppercase"
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            Platform Capabilities
          </motion.span>
          <h2 className="text-3xl md:text-4xl font-bold mb-4 tracking-tight">
            Decision-First Platform
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto text-lg">
            Move beyond dashboards. Every feature is designed to help you decide faster, 
            with more clarity, and better understanding of consequences.
          </p>
        </div>
        
        <div ref={featuresRef} className="grid md:grid-cols-3 gap-6 lg:gap-8">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Link key={feature.title} href={feature.href} className="feature-card">
                <InteractiveCard hover="lift" className="h-full py-8">
                  <div className="px-6">
                    <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center mb-6">
                      <Icon className="h-7 w-7 text-primary" />
                    </div>
                    <h3 className="text-xl font-semibold mb-3 flex items-center gap-2 group">
                      {feature.title}
                      <ArrowRight className="h-4 w-4 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all text-primary" />
                    </h3>
                    <p className="text-muted-foreground leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </InteractiveCard>
              </Link>
            );
          })}
        </div>
      </section>
      
      {/* Value Proposition */}
      <section className="border-t bg-gradient-to-b from-secondary/50 to-background">
        <div className="container py-20 md:py-28">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-16">
              <motion.span 
                className="inline-block text-sm font-semibold text-primary mb-3 tracking-wide uppercase"
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
              >
                Why Choose Us
              </motion.span>
              <h2 className="text-3xl md:text-4xl font-bold tracking-tight">
                Built for Decisions, Not Displays
              </h2>
            </div>
            
            <div ref={valueRef} className="grid md:grid-cols-3 gap-6">
              {valueProps.map((item) => {
                const Icon = item.icon;
                return (
                  <Card key={item.title} className="value-card bg-background border-border/60">
                    <CardContent className="pt-8 pb-6">
                      <div className={`w-12 h-12 rounded-xl bg-secondary flex items-center justify-center mb-5`}>
                        <Icon className={`h-6 w-6 ${item.color}`} />
                      </div>
                      <h3 className="font-semibold text-lg mb-2">{item.title}</h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {item.description}
                      </p>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="border-t">
        <div className="container py-20">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-2xl md:text-3xl font-bold mb-4">
              Ready to take control of water risk?
            </h2>
            <p className="text-muted-foreground mb-8">
              Start with a risk assessment for your zone and discover what actions could help.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button asChild size="lg" className="gap-2">
                <Link href="/risk">
                  <BarChart3 className="h-4 w-4" />
                  View Risk Status
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="gap-2">
                <Link href="/actions">
                  <Zap className="h-4 w-4" />
                  Browse Actions
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="border-t py-10 bg-secondary/30">
        <div className="container text-center">
          <div className="flex items-center justify-center gap-2 mb-3">
            <Droplets className="h-5 w-5 text-primary" />
            <span className="font-semibold">Water Risk Platform</span>
          </div>
          <p className="text-sm text-muted-foreground">
            Decision Intelligence for Drought Management
          </p>
          <p className="text-xs text-muted-foreground mt-2">
            Pilot Zones: Mexico City (CDMX) • Monterrey
          </p>
        </div>
      </footer>
    </div>
  );
}
