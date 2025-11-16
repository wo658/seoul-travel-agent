/**
 * Type definitions for the application
 *
 * This file imports types from the auto-generated OpenAPI schema (api.d.ts)
 * to ensure Single Source of Truth with the backend API.
 *
 * 🚫 DO NOT manually define API request/response types here!
 * ✅ All API types must come from the OpenAPI schema
 */

// ============================================================================
// Import auto-generated API types
// ============================================================================

import type { components } from './api';

// ============================================================================
// API Request/Response Types (from OpenAPI schema)
// ============================================================================

// ----- Travel Plan Generation -----
export type GenerateTravelPlanRequest = components['schemas']['GenerateTravelPlanRequest'];
export type PlanFormData = GenerateTravelPlanRequest; // Alias for form compatibility

// ----- Travel Plan Review/Modification -----
export type ReviewTravelPlanRequest = components['schemas']['ReviewTravelPlanRequest'];
export type ModifyPlanRequest = ReviewTravelPlanRequest; // Backward compatibility alias

// ----- API Responses -----
export type TravelPlanApiResponse = components['schemas']['app__ai__ai_schemas__TravelPlanResponse'];
export type GeneratePlanApiResponse = TravelPlanApiResponse; // Backward compatibility alias

// ----- Plan CRUD Operations -----
// export type TravelPlanCreate = components['schemas']['TravelPlanCreate']; // Not available in OpenAPI schema
export type TravelPlanUpdate = components['schemas']['TravelPlanUpdate'];
export type PlanResponse = components['schemas']['app__plan__plan_schemas__TravelPlanResponse'];
export type PlannerPlanCreate = components['schemas']['PlannerPlanCreate'];

// ----- Authentication -----
export type UserCreate = components['schemas']['UserCreate'];
export type UserLogin = components['schemas']['UserLogin'];
export type UserResponse = components['schemas']['UserResponse'];
export type Token = components['schemas']['Token'];

// ----- Validation Errors -----
export type ValidationError = components['schemas']['ValidationError'];
export type HTTPValidationError = components['schemas']['HTTPValidationError'];

// ============================================================================
// API Response Extended Types
// These types extend the OpenAPI schema with proper structure
// ============================================================================

/**
 * Itinerary structure from API response
 */
export interface PlanItinerary {
  total_days: number;
  total_cost?: number;
  days?: DayItinerary[];
}

/**
 * Recommendations structure from API response
 */
export interface PlanRecommendations {
  accommodation?: Accommodation | null;
  [key: string]: unknown;
}

/**
 * Extended PlanResponse with properly typed itinerary and recommendations
 */
export interface TypedPlanResponse extends Omit<PlanResponse, 'itinerary' | 'recommendations'> {
  itinerary?: PlanItinerary | null;
  recommendations?: PlanRecommendations | null;
}

// ============================================================================
// Frontend-specific Travel Plan Types
// These types represent the frontend's internal data structure
// ============================================================================

/**
 * Activity within a day's itinerary
 */
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

/**
 * Single day's itinerary
 */
export interface DayItinerary {
  day: number;
  date: string; // YYYY-MM-DD
  theme: string;
  activities: Activity[];
  daily_cost: number;
}

/**
 * Accommodation information
 */
export interface Accommodation {
  name: string;
  type: string;
  location: string;
  cost_per_night: number;
  total_nights: number;
  total_cost: number;
  description?: string;
}

/**
 * Complete travel plan structure (frontend representation)
 */
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

// ============================================================================
// Re-export frontend-specific types
// ============================================================================

// ============================================================================
// Type Guards
// ============================================================================

/**
 * Type guard to check if value is PlanItinerary
 */
export function isPlanItinerary(value: unknown): value is PlanItinerary {
  if (!value || typeof value !== 'object') return false;
  const obj = value as Record<string, unknown>;
  return typeof obj.total_days === 'number';
}

/**
 * Type guard to check if value is PlanRecommendations
 */
export function isPlanRecommendations(value: unknown): value is PlanRecommendations {
  return value !== null && typeof value === 'object';
}

/**
 * Safely cast PlanResponse to TypedPlanResponse
 */
export function toTypedPlanResponse(plan: PlanResponse): TypedPlanResponse {
  return {
    ...plan,
    itinerary: isPlanItinerary(plan.itinerary) ? plan.itinerary : null,
    recommendations: isPlanRecommendations(plan.recommendations) ? plan.recommendations : null,
  };
}

/**
 * Type guard to check if value has PlannerPlanCreate structure
 */
export function isPlannerPlanCreate(value: unknown): value is PlannerPlanCreate {
  if (!value || typeof value !== 'object') return false;
  const obj = value as Record<string, unknown>;
  return (
    typeof obj.title === 'string' &&
    typeof obj.total_days === 'number' &&
    typeof obj.total_cost === 'number' &&
    Array.isArray(obj.itinerary)
  );
}

/**
 * Safely convert Record<string, unknown> to PlannerPlanCreate for API
 * Returns undefined if validation fails
 */
export function toPlannerPlanCreate(plan: Record<string, unknown>): PlannerPlanCreate | undefined {
  if (isPlannerPlanCreate(plan)) {
    return plan;
  }
  return undefined;
}

/**
 * Convert TravelPlan to Record<string, unknown> for API compatibility
 */
export function travelPlanToRecord(plan: TravelPlan): Record<string, unknown> {
  return {
    id: plan.id,
    title: plan.title,
    total_days: plan.total_days,
    total_cost: plan.total_cost,
    days: plan.days,
    accommodation: plan.accommodation,
    tips: plan.tips,
    created_at: plan.created_at,
  };
}

/**
 * Convert PlanItinerary or TypedPlanResponse to Record<string, unknown>
 */
export function planToRecord(plan: PlanItinerary | TypedPlanResponse): Record<string, unknown> {
  // If it's a PlanItinerary
  if ('total_days' in plan && !('id' in plan)) {
    const itinerary = plan as PlanItinerary;
    return {
      total_days: itinerary.total_days,
      total_cost: itinerary.total_cost,
      days: itinerary.days,
    };
  }

  // If it's a TypedPlanResponse
  const response = plan as TypedPlanResponse;
  return {
    id: response.id,
    user_id: response.user_id,
    title: response.title,
    description: response.description,
    itinerary: response.itinerary,
    recommendations: response.recommendations,
    start_date: response.start_date,
    end_date: response.end_date,
    created_at: response.created_at,
    updated_at: response.updated_at,
  };
}

// ============================================================================
// Re-export frontend-specific types
// ============================================================================

// Plan viewer types (드래그앤드롭, 편집 기능)
export * from './plan-viewer';

// Planner API response types (백엔드 실제 응답 구조)
export * from './planner-api';
