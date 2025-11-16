import React from 'react';
import { View, ActivityIndicator } from 'react-native';
import { Card, CardContent } from './card';
import { Text } from './text';
import { Button, buttonTextVariants } from './button';
import { cn } from '@/lib/utils';
import { AlertCircle } from '@/lib/icons';

// ============================================================================
// LoadingState
// ============================================================================

export interface LoadingStateProps {
  size?: 'small' | 'large';
  message?: string;
  variant?: 'primary' | 'white' | 'default';
  className?: string;
}

const variantColors = {
  primary: 'hsl(var(--primary))',
  white: '#ffffff',
  default: undefined,
};

export function LoadingState({ size = 'large', message, variant = 'default', className }: LoadingStateProps) {
  return (
    <View className={cn('py-12 items-center gap-3', className)}>
      <ActivityIndicator size={size} color={variantColors[variant]} />
      {message && (
        <Text className={cn('text-base text-muted-foreground', variant === 'white' && 'text-white', size === 'small' && 'text-sm mt-2')}>
          {message}
        </Text>
      )}
    </View>
  );
}

// ============================================================================
// ErrorState
// ============================================================================

export interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  retryText?: string;
  variant?: 'inline' | 'card' | 'full';
  className?: string;
}

export function ErrorState({ title = '오류가 발생했습니다', message, onRetry, retryText = '다시 시도', variant = 'card', className }: ErrorStateProps) {
  if (variant === 'inline') {
    return (
      <View className={cn('bg-destructive/10 border-l-4 border-destructive p-4', className)}>
        <Text className="text-sm text-destructive">{message}</Text>
      </View>
    );
  }

  const content = (
    <View className="items-center gap-3">
      <AlertCircle className="text-destructive" size={32} />
      {title && <Text className="text-base font-semibold text-destructive">{title}</Text>}
      <Text className="text-sm text-muted-foreground text-center">{message}</Text>
      {onRetry && (
        <Button onPress={onRetry} className="mt-2">
          <Text className={buttonTextVariants()}>{retryText}</Text>
        </Button>
      )}
    </View>
  );

  if (variant === 'full') {
    return (
      <View className={cn('flex-1 items-center justify-center p-6', className)}>
        <Card className="bg-destructive/5 border-destructive/20 w-full">
          <CardContent className="py-6">{content}</CardContent>
        </Card>
      </View>
    );
  }

  return (
    <View className={cn('py-8', className)}>
      <Card className="bg-destructive/5 border-destructive/20">
        <CardContent className="py-6">{content}</CardContent>
      </Card>
    </View>
  );
}

// ============================================================================
// EmptyState
// ============================================================================

export interface EmptyStateProps {
  icon?: React.ComponentType<{ size?: number; className?: string }>;
  title?: string;
  message: string;
  action?: { label: string; onPress: () => void };
  variant?: 'simple' | 'card';
  className?: string;
}

export function EmptyState({ icon: Icon, title, message, action, variant = 'simple', className }: EmptyStateProps) {
  const content = (
    <View className="items-center gap-3">
      {Icon && <Icon className="text-muted-foreground" size={48} />}
      {title && <Text className="text-lg font-semibold text-foreground">{title}</Text>}
      <Text className="text-base text-center text-muted-foreground">{message}</Text>
      {action && (
        <Button onPress={action.onPress} className="mt-2">
          <Text className={buttonTextVariants()}>{action.label}</Text>
        </Button>
      )}
    </View>
  );

  if (variant === 'card') {
    return (
      <Card className={className}>
        <CardContent className="py-8">{content}</CardContent>
      </Card>
    );
  }

  return <View className={cn('py-12 items-center gap-3', className)}>{content}</View>;
}
