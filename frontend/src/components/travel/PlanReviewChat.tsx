import React, { useState } from 'react';
import { View, ScrollView } from 'react-native';
import { MessageBubble, MessageInput } from '@/components/chat';
import { LoadingState, ErrorState } from '@/components/ui';
import { aiPlansApi } from '@/lib/api';

export interface PlanReviewChatProps {
  planId?: number;
  originalPlan: Record<string, unknown>;
  onPlanUpdated?: (updatedPlan: Record<string, unknown>) => void;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

/**
 * PlanReviewChat - Chat component for reviewing and modifying travel plans
 *
 * Allows users to provide feedback and get AI-powered modifications
 * to their travel plans through a conversational interface.
 *
 * @example
 * ```tsx
 * <PlanReviewChat
 *   planId={123}
 *   originalPlan={planData}
 *   onPlanUpdated={(updated) => console.log(updated)}
 * />
 * ```
 */
export function PlanReviewChat({
  planId,
  originalPlan,
  onPlanUpdated,
}: PlanReviewChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'system',
      content: '여행 계획에 대한 피드백을 주시면 AI가 계획을 수정해드립니다.',
      timestamp: new Date(),
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [iteration, setIteration] = useState(0);

  const handleSendMessage = async (userMessage: string) => {
    // Add user message
    const userMsgId = Date.now().toString();
    const userChatMessage: ChatMessage = {
      id: userMsgId,
      role: 'user',
      content: userMessage,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userChatMessage]);

    setLoading(true);
    setError(null);

    try {
      // Call review API (uses openapi-fetch for automatic typing)
      // Pass planId to save modifications to database
      const response = await aiPlansApi.review(
        userMessage,
        originalPlan,
        iteration,
        planId  // Pass planId to save to database
      );

      // Add assistant response
      const assistantMsgId = (Date.now() + 1).toString();
      const assistantMessage: ChatMessage = {
        id: assistantMsgId,
        role: 'assistant',
        content: '계획이 수정되었습니다. 변경사항을 확인해주세요.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Update iteration count
      setIteration((prev) => prev + 1);

      // Notify parent of plan update
      if (onPlanUpdated && response.plan) {
        console.log('✅ Plan modified by AI, notifying parent component');
        onPlanUpdated(response.plan);
      } else {
        console.warn('⚠️ No onPlanUpdated callback or no plan in response');
      }
    } catch (err) {
      console.error('Failed to review plan:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to review plan';
      setError(errorMessage);

      // Add error message to chat
      const errorMsgId = (Date.now() + 2).toString();
      const errorChatMessage: ChatMessage = {
        id: errorMsgId,
        role: 'system',
        content: `오류가 발생했습니다: ${errorMessage}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorChatMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="flex-1">
      {/* Chat Messages */}
      <ScrollView className="flex-1 p-4">
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            role={msg.role}
            content={msg.content}
            timestamp={msg.timestamp}
          />
        ))}

        {/* Loading Indicator */}
        {loading && (
          <LoadingState
            size="small"
            message="AI가 계획을 수정하고 있습니다..."
            className="py-4"
          />
        )}

        {/* Error State */}
        {error && (
          <ErrorState
            message={error}
            variant="inline"
            className="mb-4"
          />
        )}
      </ScrollView>

      {/* Message Input */}
      <MessageInput
        onSend={handleSendMessage}
        disabled={loading}
        placeholder="계획 수정 요청을 입력하세요..."
      />
    </View>
  );
}
