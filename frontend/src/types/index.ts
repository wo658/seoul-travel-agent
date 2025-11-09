/**
 * Type definitions for the application
 */

// ============================================================================
// Travel Plan Types
// ============================================================================

export interface PlanFormData {
  user_request: string;
  start_date: string; // YYYY-MM-DD
  end_date: string; // YYYY-MM-DD
  budget?: number;
  interests: string[];
}

export interface Activity {
  time: string; // HH:MM format
  venue_name: string;
  venue_type: 'attraction' | 'restaurant' | 'accommodation' | 'cafe' | 'shopping';
  duration_minutes: number;
  cost: number;
  description: string;
  tips?: string;
  location?: {
    lat: number;
    lng: number;
    address: string;
  };
}

export interface DayItinerary {
  day: number;
  date: string; // YYYY-MM-DD
  theme: string;
  activities: Activity[];
  daily_cost: number;
}

export interface Accommodation {
  name: string;
  type: string;
  location: string;
  cost_per_night: number;
  total_nights: number;
  total_cost: number;
  description?: string;
}

export interface TravelPlan {
  id?: string;
  title: string;
  total_days: number;
  total_cost: number;
  days: DayItinerary[];
  accommodation?: Accommodation;
  tips?: string[];
  created_at?: string;
}

export interface GeneratePlanApiRequest {
  user_request: string;
  start_date: string;
  end_date: string;
  budget?: number;
  interests?: string[];
}

export interface GeneratePlanApiResponse {
  plan: TravelPlan;
}

export interface ModifyPlanRequest {
  user_feedback: string;
  iteration: number;
}

export interface ModifyPlanResponse {
  plan: TravelPlan;
}

// ============================================================================
// Chat Types
// ============================================================================

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
  travel_plan?: TravelPlan;
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

// Re-export plan viewer types
export * from './plan-viewer';

// Re-export planner API types
export * from './planner-api';
