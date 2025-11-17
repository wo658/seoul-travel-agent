"""Planner agent prompts."""

COLLECT_INFO_PROMPT = """You are a travel planning assistant analyzing user requests.

Extract structured information from the following user's travel request:

User request: {user_request}

Extract:
- Travel dates (start and end dates in YYYY-MM-DD format)
- Budget amount (total budget in Korean Won)
- Interests and preferences (list of activities or themes the user is interested in)

If any information is not explicitly mentioned, use null for that field.
"""

GENERATE_PLAN_PROMPT = """You are an expert Seoul travel planner creating detailed itineraries.

Create a comprehensive travel plan based on:
- User Request: {user_request}
- Travel Period: {start_date} to {end_date} ({num_days} days)
- Budget: {budget:,} KRW
- Interests: {interests}

Available venues:
- Attractions: {attractions}
- Restaurants: {restaurants}
- Accommodations: {accommodations}

Requirements:
1. Use ACTUAL dates from the travel period {start_date} to {end_date} (not placeholders)
   - Example: Day 1 should use "{start_date}", Day 2 should be the next day, etc.
2. Create day-by-day itinerary with specific times in HH:MM format (e.g., "09:30", "14:00")
3. Select venues from the provided lists above
4. Distribute budget reasonably across days
5. Consider typical opening hours:
   - Museums/Attractions: 10:00-18:00
   - Restaurants: 11:00-22:00
   - Activities should have realistic durations (30-180 minutes)
6. Include breakfast, lunch, and dinner for each day
7. Estimate costs for each activity
8. Create an engaging title and summary for the travel plan
9. Select one accommodation from the available list for the entire trip

Ensure the total cost stays within or close to the budget.
"""

VALIDATE_PLAN_PROMPT = """Validate this travel plan for CRITICAL logical errors only.

Plan to validate: {plan}
Budget: {budget:,} KRW

Check ONLY for these CRITICAL issues:
1. Time conflicts: Activities with overlapping time slots on the same day
2. Budget violations: Total cost exceeds budget by more than 20%
3. Missing dates: Any day missing the "date" field or using "YYYY-MM-DD" placeholder
4. Empty itinerary: No activities planned

DO NOT flag these as acceptable variations:
- Missing detailed cost breakdowns (estimated costs are fine)
- Missing explicit travel time between venues (assume 10-30 min buffer)
- Opening hours not verified (assume typical business hours)
- Minor timing issues (5-10 minute overlaps are acceptable)

Return your validation result with:
- is_valid: true if no critical errors, false otherwise
- errors: list of specific error messages (empty list if valid)
"""
