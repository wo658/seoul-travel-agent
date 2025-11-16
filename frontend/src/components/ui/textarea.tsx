import * as React from 'react';
import { TextInput as RNTextInput } from 'react-native';
import { cn } from '@/lib/utils';

type TextAreaProps = React.ComponentPropsWithoutRef<typeof RNTextInput> & {
  className?: string;
};

const TextArea = React.forwardRef<
  React.ElementRef<typeof RNTextInput>,
  TextAreaProps
>(({ className, placeholderClassName, ...props }, ref) => {
  return (
    <RNTextInput
      ref={ref}
      multiline
      textAlignVertical="top"
      className={cn(
        'web:flex min-h-[80px] native:min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-base native:text-lg text-foreground placeholder:text-muted-foreground web:ring-offset-background web:focus-visible:outline-none web:focus-visible:ring-2 web:focus-visible:ring-ring web:focus-visible:ring-offset-2',
        props.editable === false && 'opacity-50 web:cursor-not-allowed',
        className
      )}
      placeholderClassName={cn('text-muted-foreground', placeholderClassName)}
      {...props}
    />
  );
});

TextArea.displayName = 'TextArea';

export { TextArea };
export type { TextAreaProps };
