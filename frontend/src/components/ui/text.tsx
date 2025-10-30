import * as React from 'react';
import { Text as RNText } from 'react-native';
import * as Slot from '@rn-primitives/slot';
import { cn } from '@/lib/utils';

const Text = React.forwardRef<
  React.ElementRef<typeof RNText>,
  React.ComponentPropsWithoutRef<typeof RNText> & {
    asChild?: boolean;
  }
>(({ className, asChild = false, ...props }, ref) => {
  const Component = asChild ? Slot.Text : RNText;
  return (
    <Component
      className={cn('text-base text-foreground web:select-text', className)}
      ref={ref}
      {...props}
    />
  );
});
Text.displayName = 'Text';

export { Text };
