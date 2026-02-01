'use client';

import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { motion, HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  [
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-semibold",
    "transition-all duration-200 ease-out",
    "disabled:pointer-events-none disabled:opacity-50",
    "[&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0",
    "outline-none focus-visible:ring-2 focus-visible:ring-primary/30 focus-visible:ring-offset-2",
    "active:scale-[0.98]",
  ].join(" "),
  {
    variants: {
      variant: {
        default: [
          "bg-primary text-primary-foreground",
          "shadow-sm shadow-primary/20",
          "hover:bg-primary/90 hover:shadow-md hover:shadow-primary/25",
        ].join(" "),
        destructive: [
          "bg-destructive text-white",
          "shadow-sm shadow-destructive/20",
          "hover:bg-destructive/90 hover:shadow-md hover:shadow-destructive/25",
        ].join(" "),
        outline: [
          "border border-border bg-background",
          "shadow-xs",
          "hover:bg-secondary hover:border-border/80",
        ].join(" "),
        secondary: [
          "bg-secondary text-secondary-foreground",
          "hover:bg-secondary/80",
        ].join(" "),
        ghost: [
          "hover:bg-secondary hover:text-secondary-foreground",
        ].join(" "),
        link: [
          "text-primary underline-offset-4",
          "hover:underline",
        ].join(" "),
        // New premium variant with glow
        glow: [
          "bg-primary text-primary-foreground",
          "shadow-md shadow-primary/30",
          "hover:shadow-lg hover:shadow-primary/40",
          "hover:bg-primary/95",
        ].join(" "),
      },
      size: {
        default: "h-10 px-5 py-2",
        xs: "h-7 gap-1 rounded-lg px-2.5 text-xs",
        sm: "h-9 rounded-lg gap-1.5 px-4",
        lg: "h-12 rounded-xl px-8 text-base",
        xl: "h-14 rounded-xl px-10 text-lg",
        icon: "size-10",
        "icon-xs": "size-7 rounded-lg [&_svg:not([class*='size-'])]:size-3.5",
        "icon-sm": "size-9 rounded-lg",
        "icon-lg": "size-12 rounded-xl",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

interface ButtonProps
  extends React.ComponentProps<"button">,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

function Button({
  className,
  variant = "default",
  size = "default",
  asChild = false,
  ...props
}: ButtonProps) {
  const Comp = asChild ? Slot : "button";

  return (
    <Comp
      data-slot="button"
      data-variant={variant}
      data-size={size}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

// Animated button with Framer Motion
interface AnimatedButtonProps
  extends Omit<HTMLMotionProps<"button">, 'children'>,
    VariantProps<typeof buttonVariants> {
  children: React.ReactNode;
}

const AnimatedButton = React.forwardRef<HTMLButtonElement, AnimatedButtonProps>(
  ({ className, variant = "default", size = "default", children, ...props }, ref) => {
    return (
      <motion.button
        ref={ref}
        data-slot="button"
        data-variant={variant}
        data-size={size}
        className={cn(buttonVariants({ variant, size, className }))}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        transition={{ duration: 0.15, ease: [0.25, 0.1, 0.25, 1] }}
        {...props}
      >
        {children}
      </motion.button>
    );
  }
);
AnimatedButton.displayName = "AnimatedButton";

export { Button, AnimatedButton, buttonVariants };
