import React, { useState } from 'react';
import { View, Pressable, KeyboardAvoidingView, Platform } from 'react-native';
import { Input } from '@/components/ui';
import { cn } from '@/lib/utils';
import { Send } from '@/lib/icons';

export interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
  className?: string;
}

/**
 * MessageInput - Chat message input component
 * Text input with send button
 *
 * @example
 * ```tsx
 * <MessageInput
 *   onSend={(msg) => console.log(msg)}
 *   placeholder="Type a message..."
 * />
 * ```
 */
export function MessageInput({
  onSend,
  disabled = false,
  placeholder = '메시지를 입력하세요...',
  className
}: MessageInputProps) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
    >
      <View
        className={cn(
          'flex-row items-center gap-2 p-4 bg-background border-t border-border',
          className
        )}
      >
        <Input
          value={message}
          onChangeText={setMessage}
          placeholder={placeholder}
          className="flex-1"
          editable={!disabled}
          multiline
          maxLength={1000}
          onSubmitEditing={handleSend}
          returnKeyType="send"
        />

        <Pressable
          onPress={handleSend}
          disabled={disabled || !message.trim()}
          className={cn(
            'w-12 h-12 rounded-full items-center justify-center',
            disabled || !message.trim()
              ? 'bg-muted'
              : 'bg-primary active:opacity-80'
          )}
        >
          <Send
            size={20}
            className={cn(
              disabled || !message.trim()
                ? 'text-muted-foreground'
                : 'text-primary-foreground'
            )}
          />
        </Pressable>
      </View>
    </KeyboardAvoidingView>
  );
}
