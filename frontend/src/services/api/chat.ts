/**
 * Travel Plan API service
 *
 * ✅ Fully automated with openapi-fetch
 * ✅ Type inference from OpenAPI schema
 * ✅ Single Source of Truth: Backend OpenAPI spec
 */

import { aiPlansApi } from '@/lib/api';

/**
 * Generate travel plan using AI Planner Agent
 *
 * Now uses openapi-fetch for automatic type inference
 *
 * @param data - Request body (automatically typed)
 * @param userId - User ID
 * @param saveToDb - Whether to save to database
 * @returns Travel plan response (automatically typed)
 */
export async function generatePlan(
  data: {
    user_request: string;
    start_date: string;
    end_date: string;
    budget?: number | null;
    interests: string[];
  },
  userId: number = 1,
  saveToDb: boolean = true
) {
  const result = await aiPlansApi.generate(data, userId, saveToDb);

  // Backend returns { plan: dict } where plan might be in PlannerResponse format
  // We need to ensure it has the correct TravelPlan structure
  if (result.plan && typeof result.plan === 'object') {
    const planObj = result.plan as Record<string, unknown>;

    // If plan has 'type' and 'plan' properties, it's a PlannerResponse
    if ('type' in planObj && 'plan' in planObj) {
      const { mapPlannerResponseToTravelPlan } = await import('@/lib/utils/plan-mapper');
      const { travelPlanToRecord } = await import('@/types');
      const mappedPlan = mapPlannerResponseToTravelPlan(planObj);
      // Convert TravelPlan back to Record<string, unknown> for API compatibility
      result.plan = travelPlanToRecord(mappedPlan);
    }

    // Ensure plan has required TravelPlan fields
    // If it has itinerary but not days, copy itinerary to days
    const currentPlan = result.plan as Record<string, unknown>;
    if (!currentPlan.days && currentPlan.itinerary) {
      currentPlan.days = currentPlan.itinerary;
    }
  }

  return result;
}
