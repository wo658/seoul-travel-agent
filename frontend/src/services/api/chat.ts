/**
 * Chat API service
 * Handles all chat-related API calls including streaming
 */

import type {
  Conversation,
  CreateConversationRequest,
  CreateConversationResponse,
  SendMessageRequest,
  StreamChunk,
  GeneratePlanRequest,
  GeneratePlanResponse,
  ConversationListItem,
} from '@/types/chat';

// TODO: Replace with actual backend URL from environment
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Create a new conversation
 */
export async function createConversation(
  data: CreateConversationRequest
): Promise<CreateConversationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/ai/conversations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Failed to create conversation: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get conversation by ID
 */
export async function getConversation(id: string): Promise<Conversation> {
  const response = await fetch(`${API_BASE_URL}/api/ai/conversations/${id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get conversation: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get all conversations
 */
export async function getConversations(): Promise<ConversationListItem[]> {
  const response = await fetch(`${API_BASE_URL}/api/ai/conversations`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get conversations: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Stream chat messages using Server-Sent Events (SSE)
 * Note: React Native doesn't support ReadableStream natively
 * This is a simplified implementation that will be enhanced with a proper SSE library
 */
export async function* streamChatMessage(
  conversationId: string,
  data: SendMessageRequest
): AsyncGenerator<StreamChunk> {
  // For now, we'll use the non-streaming endpoint and simulate streaming
  // In production, you should use a library like react-native-sse or eventsource-polyfill
  const response = await fetch(
    `${API_BASE_URL}/api/ai/conversations/${conversationId}/messages/stream`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to stream message: ${response.statusText}`);
  }

  const text = await response.text();
  const lines = text.split('\n');

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);

      if (data === '[DONE]') {
        return;
      }

      try {
        const chunk: StreamChunk = JSON.parse(data);
        yield chunk;
      } catch (e) {
        console.error('Failed to parse SSE data:', data, e);
      }
    }
  }
}

/**
 * Send a message without streaming (fallback)
 */
export async function sendMessage(
  conversationId: string,
  data: SendMessageRequest
): Promise<{ message: string }> {
  const response = await fetch(
    `${API_BASE_URL}/api/ai/conversations/${conversationId}/messages`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to send message: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Generate travel plan from conversation
 */
export async function generatePlan(
  conversationId: string,
  data?: GeneratePlanRequest
): Promise<GeneratePlanResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/ai/conversations/${conversationId}/generate-plan`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data || {}),
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to generate plan: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Delete conversation
 */
export async function deleteConversation(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/ai/conversations/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to delete conversation: ${response.statusText}`);
  }
}
