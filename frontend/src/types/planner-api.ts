/**
 * Planner Agent API 응답 타입 정의
 * Backend의 실제 응답 구조에 맞춘 타입
 */

// ============================================================================
// Planner Agent Response Types
// ============================================================================

export interface PlannerActivity {
  time: string; // HH:MM format
  venue_name: string;
  venue_type: 'attraction' | 'restaurant' | 'accommodation' | 'cafe' | 'shopping';
  duration_minutes: number;
  estimated_cost: number; // Backend uses "estimated_cost"
  notes?: string; // Backend uses "notes" instead of "description"
}

export interface PlannerDayItinerary {
  day: number;
  date: string; // YYYY-MM-DD
  theme: string;
  activities: PlannerActivity[];
  daily_cost: number;
}

export interface PlannerAccommodation {
  name: string;
  cost_per_night: number;
  total_nights: number;
  // Backend doesn't include these fields
  // type?: string;
  // location?: string;
  // total_cost?: number;
  // description?: string;
}

export interface PlannerPlan {
  title: string;
  total_days: number;
  total_cost: number;
  itinerary: PlannerDayItinerary[]; // Backend uses "itinerary" instead of "days"
  accommodation?: PlannerAccommodation;
  summary?: string; // Backend includes summary
}

export interface PlannerResponse {
  type: 'complete' | 'incomplete' | 'error';
  plan: PlannerPlan;
}
