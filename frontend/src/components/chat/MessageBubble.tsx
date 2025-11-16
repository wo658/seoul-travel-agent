import React from 'react';
import { View } from 'react-native';
import { Text, IconContainer } from '@/components/ui';
import { cn } from '@/lib/utils';
import { User, Sparkles } from '@/lib/icons';

export interface MessageBubbleProps {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: Date;
  className?: string;
}

/**
 * MessageBubble - Chat message bubble component
 * Displays messages with role-based styling
 *
 * @example
 * ```tsx
 * <MessageBubble
 *   role="user"
 *   content="Hello!"
 *   timestamp={new Date()}
 * />
 * ```
 */
export function MessageBubble({
  role,
  content,
  timestamp,
  className
}: MessageBubbleProps) {
  const isUser = role === 'user';
  const isSystem = role === 'system';

  return (
    <View
      className={cn(
        'mb-4 flex-row',
        isUser ? 'justify-end' : 'justify-start',
        className
      )}
    >
      {!isUser && !isSystem && (
        <IconContainer size="sm" variant="primary" className="mr-2">
          <Sparkles size={16} className="text-primary-foreground" />
        </IconContainer>
      )}

      <View className={cn('max-w-[80%]', isUser && 'items-end')}>
        <View
          className={cn(
            'rounded-2xl px-4 py-3',
            isUser && 'bg-primary',
            !isUser && !isSystem && 'bg-muted',
            isSystem && 'bg-secondary'
          )}
        >
          <Text
            className={cn(
              'text-base leading-5',
              isUser ? 'text-primary-foreground' : 'text-foreground',
              isSystem && 'text-secondary-foreground text-sm'
            )}
          >
            {content}
          </Text>
        </View>

        {timestamp && !isSystem && (
          <Text className="text-xs text-muted-foreground mt-1 px-2">
            {formatTime(timestamp)}
          </Text>
        )}
      </View>

      {isUser && (
        <IconContainer size="sm" variant="secondary" className="ml-2">
          <User size={16} className="text-secondary-foreground" />
        </IconContainer>
      )}
    </View>
  );
}

function formatTime(date: Date): string {
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  return `${hours}:${minutes}`;
}
