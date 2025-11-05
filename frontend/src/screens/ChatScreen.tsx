/**
 * ChatScreen - Main chat interface
 */

import React, { useRef, useEffect } from 'react';
import {
  View,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Pressable,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Text, Button, buttonTextVariants } from '@/components/ui';
import { MessageBubble, MessageInput, StreamingIndicator } from '@/components/chat';
import { useChat } from '@/hooks/useChat';
import { ArrowLeft, Sparkles } from '@/lib/icons';

export interface ChatScreenProps {
  conversationId?: string;
  onBack?: () => void;
  onPlanGenerated?: (planId: string) => void;
}

export function ChatScreen({
  conversationId,
  onBack,
  onPlanGenerated,
}: ChatScreenProps) {
  const scrollViewRef = useRef<ScrollView>(null);

  const {
    conversation,
    messages,
    isStreaming,
    streamingMessage,
    isLoading,
    error,
    sendMessage,
    createTravelPlan,
    clearError,
  } = useChat({ conversationId, autoLoad: true });

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollViewRef.current) {
      scrollViewRef.current.scrollToEnd({ animated: true });
    }
  }, [messages, streamingMessage]);

  const handleSendMessage = async (content: string) => {
    await sendMessage(content);
  };

  const handleGeneratePlan = async () => {
    const plan = await createTravelPlan();
    if (plan && onPlanGenerated) {
      onPlanGenerated(plan.plan_id);
    }
  };

  return (
    <View className="flex-1 bg-background">
      <StatusBar style="auto" />

      {/* Header */}
      <View className="flex-row items-center justify-between px-4 py-3 border-b border-border bg-card">
        <View className="flex-row items-center gap-3 flex-1">
          {onBack && (
            <Pressable
              onPress={onBack}
              className="w-10 h-10 items-center justify-center active:opacity-70"
            >
              <ArrowLeft size={24} className="text-foreground" />
            </Pressable>
          )}

          <View className="flex-1">
            <Text className="text-lg font-semibold text-foreground">
              {conversation?.title || '새 대화'}
            </Text>
            <Text className="text-xs text-muted-foreground">
              {isStreaming ? 'AI가 입력 중...' : '서울 여행 AI 어시스턴트'}
            </Text>
          </View>
        </View>

        {messages.length > 0 && (
          <Button
            variant="outline"
            size="sm"
            onPress={handleGeneratePlan}
            disabled={isLoading || isStreaming}
          >
            <View className="flex-row items-center gap-1">
              <Sparkles size={14} className="text-primary" />
              <Text className={buttonTextVariants({ variant: 'outline', size: 'sm' })}>
                여행 계획 생성
              </Text>
            </View>
          </Button>
        )}
      </View>

      {/* Error Banner */}
      {error && (
        <View className="px-4 py-3 bg-destructive">
          <View className="flex-row items-center justify-between">
            <Text className="text-sm text-destructive-foreground flex-1">
              {error}
            </Text>
            <Pressable onPress={clearError}>
              <Text className="text-sm text-destructive-foreground font-semibold">
                닫기
              </Text>
            </Pressable>
          </View>
        </View>
      )}

      {/* Messages */}
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        className="flex-1"
        keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
      >
        <ScrollView
          ref={scrollViewRef}
          className="flex-1"
          contentContainerClassName="p-4"
          onContentSizeChange={() => {
            scrollViewRef.current?.scrollToEnd({ animated: true });
          }}
        >
          {messages.length === 0 && !isStreaming && (
            <View className="flex-1 items-center justify-center py-20">
              <Sparkles size={48} className="text-muted-foreground mb-4" />
              <Text className="text-xl font-semibold text-foreground mb-2">
                서울 여행을 계획해보세요
              </Text>
              <Text className="text-base text-muted-foreground text-center px-8">
                여행 기간, 예산, 관심사를 알려주시면{'\n'}
                맞춤형 여행 계획을 만들어드립니다
              </Text>
            </View>
          )}

          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              role={message.role}
              content={message.content}
              timestamp={new Date(message.created_at)}
            />
          ))}

          {isStreaming && (
            <>
              {streamingMessage ? (
                <MessageBubble
                  role="assistant"
                  content={streamingMessage}
                />
              ) : (
                <StreamingIndicator />
              )}
            </>
          )}
        </ScrollView>

        {/* Input */}
        <MessageInput
          onSend={handleSendMessage}
          disabled={isStreaming || isLoading}
          placeholder="메시지를 입력하세요..."
        />
      </KeyboardAvoidingView>
    </View>
  );
}
