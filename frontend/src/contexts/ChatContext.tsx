/**
 * ChatContext - Global chat state management
 */

import React, { createContext, useContext, useState, useCallback } from 'react';
import type { Conversation, Message, ConversationListItem } from '@/types/chat';

export interface ChatState {
  conversations: ConversationListItem[];
  currentConversation: Conversation | null;
  isStreaming: boolean;
  streamingMessage: string;
  error: string | null;
}

export interface ChatContextValue extends ChatState {
  setConversations: (conversations: ConversationListItem[]) => void;
  setCurrentConversation: (conversation: Conversation | null) => void;
  setIsStreaming: (isStreaming: boolean) => void;
  setStreamingMessage: (message: string) => void;
  appendStreamingToken: (token: string) => void;
  resetStreamingMessage: () => void;
  addMessage: (message: Message) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

const ChatContext = createContext<ChatContextValue | undefined>(undefined);

export interface ChatProviderProps {
  children: React.ReactNode;
}

export function ChatProvider({ children }: ChatProviderProps) {
  const [conversations, setConversations] = useState<ConversationListItem[]>([]);
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');
  const [error, setError] = useState<string | null>(null);

  const appendStreamingToken = useCallback((token: string) => {
    setStreamingMessage((prev) => prev + token);
  }, []);

  const resetStreamingMessage = useCallback(() => {
    setStreamingMessage('');
  }, []);

  const addMessage = useCallback((message: Message) => {
    setCurrentConversation((prev) => {
      if (!prev) return null;
      return {
        ...prev,
        messages: [...prev.messages, message],
      };
    });
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const value: ChatContextValue = {
    conversations,
    currentConversation,
    isStreaming,
    streamingMessage,
    error,
    setConversations,
    setCurrentConversation,
    setIsStreaming,
    setStreamingMessage,
    appendStreamingToken,
    resetStreamingMessage,
    addMessage,
    setError,
    clearError,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
}

export function useChatContext() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
}
