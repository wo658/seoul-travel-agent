/**
 * Chat types for the application
 */

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  model?: string;
  tokens_used?: number;
  finish_reason?: string;
  created_at: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  travel_plan_id?: string;
  title: string;
  status: 'active' | 'completed' | 'archived';
  created_at: string;
  updated_at: string;
  messages: Message[];
  travel_plan?: any; // TODO: Define TravelPlan type
}

export interface CreateConversationRequest {
  initial_message: string;
}

export interface CreateConversationResponse {
  conversation_id: string;
  message: Message;
}

export interface SendMessageRequest {
  content: string;
}

export interface StreamChunk {
  token: string;
  finish_reason?: string;
}

export interface GeneratePlanRequest {
  preferences?: Record<string, any>;
}

export interface GeneratePlanResponse {
  plan_id: string;
  itinerary: any; // TODO: Define Itinerary type
}

export interface ConversationListItem {
  id: string;
  title: string;
  status: 'active' | 'completed' | 'archived';
  last_message?: string;
  created_at: string;
  updated_at: string;
}
