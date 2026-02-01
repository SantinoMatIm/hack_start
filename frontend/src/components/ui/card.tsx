'use client';

import * as React from "react";
import { motion, HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";

// Base Card - standard static card
function Card({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card"
      className={cn(
        "bg-card text-card-foreground flex flex-col gap-6 rounded-2xl border border-border/60 py-6",
        "shadow-sm transition-shadow duration-300",
        className
      )}
      {...props}
    />
  );
}

// Interactive Card with hover animations
interface InteractiveCardProps extends Omit<HTMLMotionProps<"div">, 'children'> {
  children: React.ReactNode;
  hover?: 'lift' | 'glow' | 'border' | 'none';
}

const InteractiveCard = React.forwardRef<HTMLDivElement, InteractiveCardProps>(
  ({ className, hover = 'lift', children, ...props }, ref) => {
    const hoverStyles = {
      lift: 'hover:shadow-lg hover:-translate-y-1',
      glow: 'hover:shadow-glow',
      border: 'hover:border-primary/30',
      none: '',
    };

    return (
      <motion.div
        ref={ref}
        data-slot="card"
        className={cn(
          "bg-card text-card-foreground flex flex-col gap-6 rounded-2xl border border-border/60 py-6",
          "shadow-sm cursor-pointer",
          "transition-all duration-300 ease-out",
          hoverStyles[hover],
          className
        )}
        whileHover={{ scale: hover === 'lift' ? 1.01 : 1 }}
        whileTap={{ scale: 0.995 }}
        transition={{ duration: 0.2, ease: [0.25, 0.1, 0.25, 1] }}
        {...props}
      >
        {children}
      </motion.div>
    );
  }
);
InteractiveCard.displayName = "InteractiveCard";

// Glass Card variant
function GlassCard({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card"
      className={cn(
        "flex flex-col gap-6 rounded-2xl py-6",
        "glass border-white/20",
        "shadow-lg",
        className
      )}
      {...props}
    />
  );
}

// Highlighted Card (for selected/active states)
interface HighlightedCardProps extends React.ComponentProps<"div"> {
  variant?: 'primary' | 'success' | 'warning' | 'danger';
}

function HighlightedCard({ 
  className, 
  variant = 'primary',
  ...props 
}: HighlightedCardProps) {
  const variantStyles = {
    primary: 'border-primary/30 bg-primary/[0.02] shadow-[0_0_0_1px_rgba(37,99,235,0.1)]',
    success: 'border-emerald-500/30 bg-emerald-50/50',
    warning: 'border-amber-500/30 bg-amber-50/50',
    danger: 'border-red-500/30 bg-red-50/50',
  };

  return (
    <div
      data-slot="card"
      className={cn(
        "flex flex-col gap-6 rounded-2xl border py-6",
        "shadow-sm transition-all duration-300",
        variantStyles[variant],
        className
      )}
      {...props}
    />
  );
}

function CardHeader({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-header"
      className={cn(
        "@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start gap-1.5 px-6 has-data-[slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6",
        className
      )}
      {...props}
    />
  );
}

function CardTitle({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-title"
      className={cn(
        "text-lg leading-tight font-semibold tracking-tight text-foreground",
        className
      )}
      {...props}
    />
  );
}

function CardDescription({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-description"
      className={cn("text-muted-foreground text-sm leading-relaxed", className)}
      {...props}
    />
  );
}

function CardAction({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-action"
      className={cn(
        "col-start-2 row-span-2 row-start-1 self-start justify-self-end",
        className
      )}
      {...props}
    />
  );
}

function CardContent({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-content"
      className={cn("px-6", className)}
      {...props}
    />
  );
}

function CardFooter({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card-footer"
      className={cn("flex items-center px-6 [.border-t]:pt-6", className)}
      {...props}
    />
  );
}

export {
  Card,
  InteractiveCard,
  GlassCard,
  HighlightedCard,
  CardHeader,
  CardFooter,
  CardTitle,
  CardAction,
  CardDescription,
  CardContent,
};
