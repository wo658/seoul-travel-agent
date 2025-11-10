/**
 * Travel Plan API service
 *
 * Uses OpenAPI-generated types for type safety and Single Source of Truth
 */

import type {
  // OpenAPI-generated types (Single Source of Truth)
  GenerateTravelPlanRequest,
  TravelPlanApiResponse,
} from '@/types';

// TODO: Replace with actual backend URL from environment
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Generate travel plan directly from form data
 *
 * @param data - Travel plan generation request (from OpenAPI schema)
 * @returns Travel plan response (from OpenAPI schema)
 */
export async function generatePlan(
  data: GenerateTravelPlanRequest
): Promise<TravelPlanApiResponse> {
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
