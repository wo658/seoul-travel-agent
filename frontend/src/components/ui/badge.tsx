import * as React from 'react';
import { View } from 'react-native';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'flex flex-row items-center rounded-full border px-2.5 py-0.5 native:px-3 native:py-1',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-primary',
        secondary: 'border-transparent bg-secondary',
        destructive: 'border-transparent bg-destructive',
        outline: 'border-border bg-transparent',
        success: 'border-transparent bg-green-500',
        warning: 'border-transparent bg-yellow-500',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

const badgeTextVariants = cva(
  'text-xs native:text-sm font-semibold',
  {
    variants: {
      variant: {
        default: 'text-primary-foreground',
        secondary: 'text-secondary-foreground',
        destructive: 'text-destructive-foreground',
        outline: 'text-foreground',
        success: 'text-white',
        warning: 'text-white',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

type BadgeProps = React.ComponentPropsWithoutRef<typeof View> & {
  variant?: VariantProps<typeof badgeVariants>['variant'];
  children?: React.ReactNode;
};

const Badge = React.forwardRef<
  React.ElementRef<typeof View>,
  BadgeProps
>(({ className, variant, ...props }, ref) => {
  return (
    <View
      className={cn(badgeVariants({ variant, className }))}
      ref={ref}
      {...props}
    />
  );
});
Badge.displayName = 'Badge';

export { Badge, badgeTextVariants, badgeVariants };
export type { BadgeProps };
