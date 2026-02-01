'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { 
  Droplets, 
  BarChart3, 
  Zap, 
  Play,
  Home
} from 'lucide-react';

const navItems = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/risk', label: 'Risk Overview', icon: BarChart3 },
  { href: '/actions', label: 'Actions', icon: Zap },
  { href: '/simulation', label: 'Simulation', icon: Play },
];

export function Navigation() {
  const pathname = usePathname();
  
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 mr-8">
          <div className="p-2 rounded-lg bg-primary/10">
            <Droplets className="h-5 w-5 text-primary" />
          </div>
          <span className="font-bold text-lg hidden sm:inline-block">
            Water Risk
          </span>
        </Link>
        
        {/* Navigation Links */}
        <nav className="flex items-center gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                  isActive 
                    ? 'bg-primary/10 text-primary' 
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                )}
              >
                <Icon className="h-4 w-4" />
                <span className="hidden md:inline-block">{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
