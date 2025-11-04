/**
 * useChat - Chat functionality hook
 */

import { useCallback, useEffect, useState } from 'react';
import { useChatContext } from '@/contexts/ChatContext';
import {
  createConversation,
  getConversation,
  getConversations,
  streamChatMessage,
  sendMessage,
  generatePlan,
} from '@/services/api/chat';
import type { Message } from '@/types/chat';

export interface UseChatOptions {
  conversationId?: string;
  autoLoad?: boolean;
}

export function useChat(options: UseChatOptions = {}) {
  const {
    currentConversation,
    setCurrentConversation,
    isStreaming,
    setIsStreaming,
    streamingMessage,
    appendStreamingToken,
    resetStreamingMessage,
    addMessage,
    conversations,
    setConversations,
    error,
    setError,
    clearError,
  } = useChatContext();

  const [isLoading, setIsLoading] = useState(false);

  // Load conversation by ID
  const loadConversation = useCallback(
    async (id: string) => {
      try {
        setIsLoading(true);
        clearError();
        const conversation = await getConversation(id);
        setCurrentConversation(conversation);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load conversation';
        setError(message);
        console.error('Load conversation error:', err);
      } finally {
        setIsLoading(false);
      }
    },
    [setCurrentConversation, setError, clearError]
  );

  // Load all conversations
  const loadConversations = useCallback(async () => {
    try {
      setIsLoading(true);
      clearError();
      const data = await getConversations();
      setConversations(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load conversations';
      setError(message);
      console.error('Load conversations error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [setConversations, setError, clearError]);

  // Create new conversation
  const startConversation = useCallback(
    async (initialMessage: string) => {
      try {
        setIsLoading(true);
        clearError();
        const response = await createConversation({ initial_message: initialMessage });
        await loadConversation(response.conversation_id);
        await loadConversations();
        return response.conversation_id;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to start conversation';
        setError(message);
        console.error('Start conversation error:', err);
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    [loadConversation, loadConversations, setError, clearError]
  );

  // Send message with streaming
  const sendStreamingMessage = useCallback(
    async (content: string) => {
      if (!currentConversation) {
        setError('No active conversation');
        return;
      }

      try {
        clearError();
        setIsStreaming(true);
        resetStreamingMessage();

        // Add user message immediately
        const userMessage: Message = {
          id: `temp-${Date.now()}`,
          conversation_id: currentConversation.id,
          role: 'user',
          content,
          created_at: new Date().toISOString(),
        };
        addMessage(userMessage);

        // Stream AI response
        const stream = streamChatMessage(currentConversation.id, { content });

        for await (const chunk of stream) {
          appendStreamingToken(chunk.token);

          if (chunk.finish_reason) {
            // Streaming complete, save final message
            const assistantMessage: Message = {
              id: `msg-${Date.now()}`,
              conversation_id: currentConversation.id,
              role: 'assistant',
              content: streamingMessage + chunk.token,
              finish_reason: chunk.finish_reason,
              created_at: new Date().toISOString(),
            };
            addMessage(assistantMessage);
            resetStreamingMessage();
          }
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to send message';
        setError(message);
        console.error('Send message error:', err);

        // Fallback to non-streaming
        try {
          const response = await sendMessage(currentConversation.id, { content });
          const assistantMessage: Message = {
            id: `msg-${Date.now()}`,
            conversation_id: currentConversation.id,
            role: 'assistant',
            content: response.message,
            created_at: new Date().toISOString(),
          };
          addMessage(assistantMessage);
        } catch (fallbackErr) {
          console.error('Fallback send message error:', fallbackErr);
        }
      } finally {
        setIsStreaming(false);
      }
    },
    [
      currentConversation,
      setIsStreaming,
      resetStreamingMessage,
      appendStreamingToken,
      addMessage,
      streamingMessage,
      setError,
      clearError,
    ]
  );

  // Generate travel plan
  const createTravelPlan = useCallback(async () => {
    if (!currentConversation) {
      setError('No active conversation');
      return null;
    }

    try {
      setIsLoading(true);
      clearError();
      const plan = await generatePlan(currentConversation.id);
      return plan;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to generate plan';
      setError(message);
      console.error('Generate plan error:', err);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [currentConversation, setError, clearError]);

  // Auto-load conversation on mount if ID provided
  useEffect(() => {
    if (options.conversationId && options.autoLoad !== false) {
      loadConversation(options.conversationId);
    }
  }, [options.conversationId, options.autoLoad, loadConversation]);

  return {
    // State
    conversation: currentConversation,
    messages: currentConversation?.messages || [],
    conversations,
    isStreaming,
    streamingMessage,
    isLoading,
    error,

    // Actions
    startConversation,
    loadConversation,
    loadConversations,
    sendMessage: sendStreamingMessage,
    createTravelPlan,
    clearError,
  };
}
