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

import type { components, operations } from './api';

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
export type TravelPlanCreate = components['schemas']['TravelPlanCreate'];
export type TravelPlanUpdate = components['schemas']['TravelPlanUpdate'];
export type PlanResponse = components['schemas']['app__plan__plan_schemas__TravelPlanResponse'];

// ----- Authentication -----
export type UserCreate = components['schemas']['UserCreate'];
export type UserLogin = components['schemas']['UserLogin'];
export type UserResponse = components['schemas']['UserResponse'];
export type Token = components['schemas']['Token'];

// ----- Validation Errors -----
export type ValidationError = components['schemas']['ValidationError'];
export type HTTPValidationError = components['schemas']['HTTPValidationError'];

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

// Plan viewer types (드래그앤드롭, 편집 기능)
export * from './plan-viewer';

// Planner API response types (백엔드 실제 응답 구조)
export * from './planner-api';
