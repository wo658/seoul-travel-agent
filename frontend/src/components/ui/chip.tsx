import * as React from 'react';
import { Pressable as RNPressable } from 'react-native';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const chipVariants = cva(
  'flex flex-row items-center justify-center rounded-full border web:transition-colors web:focus-visible:outline-none web:focus-visible:ring-2 web:focus-visible:ring-ring web:focus-visible:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'border-input bg-background web:hover:bg-accent active:bg-accent',
        selected: 'border-primary bg-primary web:hover:opacity-90 active:opacity-90',
        outline: 'border-input bg-transparent web:hover:bg-accent active:bg-accent',
      },
      size: {
        default: 'h-8 px-3 py-1 native:h-10 native:px-4 native:py-2',
        sm: 'h-6 px-2 py-0.5 native:h-8 native:px-3',
        lg: 'h-10 px-4 py-2 native:h-12 native:px-5',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

const chipTextVariants = cva(
  'text-sm native:text-base font-medium web:transition-colors',
  {
    variants: {
      variant: {
        default: 'text-foreground',
        selected: 'text-primary-foreground',
        outline: 'text-foreground',
      },
      size: {
        default: '',
        sm: 'text-xs native:text-sm',
        lg: 'text-base native:text-lg',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

type ChipProps = React.ComponentPropsWithoutRef<typeof RNPressable> & {
  variant?: VariantProps<typeof chipVariants>['variant'];
  size?: VariantProps<typeof chipVariants>['size'];
  selected?: boolean;
  children?: React.ReactNode;
};

const Chip = React.forwardRef<
  React.ElementRef<typeof RNPressable>,
  ChipProps
>(({ className, variant, size, selected, ...props }, ref) => {
  const finalVariant = selected ? 'selected' : variant;
  return (
    <RNPressable
      className={cn(chipVariants({ variant: finalVariant, size, className }))}
      ref={ref}
      role="button"
      {...props}
    />
  );
});
Chip.displayName = 'Chip';

export { Chip, chipTextVariants, chipVariants };
export type { ChipProps };
