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
  GeneratePlanApiRequest,
  GeneratePlanApiResponse,
  ModifyPlanRequest,
  ModifyPlanResponse,
} from '@/types';

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
 * Generate travel plan from conversation (legacy)
 */
export async function generatePlanFromConversation(
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
 * Generate travel plan directly from form data
 */
export async function generatePlan(
  data: GeneratePlanApiRequest
): Promise<GeneratePlanApiResponse> {
  const response = await fetch(`${API_BASE_URL}/api/ai/plans/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to generate plan: ${errorText || response.statusText}`);
  }

  const result = await response.json();

  // Backend returns { plan: dict } where plan might be in PlannerResponse format
  // We need to ensure it has the correct TravelPlan structure
  if (result.plan && typeof result.plan === 'object') {
    // If plan has 'type' and 'plan' properties, it's a PlannerResponse
    if ('type' in result.plan && 'plan' in result.plan) {
      const { mapPlannerResponseToTravelPlan } = await import('@/lib/utils/plan-mapper');
      result.plan = mapPlannerResponseToTravelPlan(result.plan);
    }

    // Ensure plan has required TravelPlan fields
    if (!result.plan.days && result.plan.itinerary) {
      result.plan.days = result.plan.itinerary;
    }
  }

  return result;
}

/**
 * Modify existing travel plan with user feedback
 */
export async function modifyPlan(
  data: ModifyPlanRequest
): Promise<ModifyPlanResponse> {
  const response = await fetch(`${API_BASE_URL}/api/ai/plans/review`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to modify plan: ${errorText || response.statusText}`);
  }

  const result = await response.json();

  // Backend returns { plan: dict } where plan might be in PlannerResponse format
  // We need to ensure it has the correct TravelPlan structure
  if (result.plan && typeof result.plan === 'object') {
    // If plan has 'type' and 'plan' properties, it's a PlannerResponse
    if ('type' in result.plan && 'plan' in result.plan) {
      const { mapPlannerResponseToTravelPlan } = await import('@/lib/utils/plan-mapper');
      result.plan = mapPlannerResponseToTravelPlan(result.plan);
    }

    // Ensure plan has required TravelPlan fields
    if (!result.plan.days && result.plan.itinerary) {
      result.plan.days = result.plan.itinerary;
    }
  }

  return result;
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
