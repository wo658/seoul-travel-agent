import React from 'react';
import { TextInput, type TextInputProps } from 'react-native';
import { cn } from '@/lib/utils';

export interface InputProps extends TextInputProps {
  className?: string;
}

/**
 * Input component with Tailwind CSS styling
 * Pure React Native implementation following shadcn/ui philosophy
 *
 * @example
 * ```tsx
 * <Input
 *   placeholder="Enter your name"
 *   value={name}
 *   onChangeText={setName}
 * />
 * ```
 */
export function Input({ className, placeholderTextColor, ...props }: InputProps) {
  return (
    <TextInput
      className={cn(
        'h-12 rounded-lg border border-input bg-background px-4 py-3 text-base text-foreground',
        className
      )}
      placeholderTextColor={placeholderTextColor || '#999'}
      {...props}
    />
  );
}
