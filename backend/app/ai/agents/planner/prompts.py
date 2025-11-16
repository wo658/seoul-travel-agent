"""Planner agent prompts."""

COLLECT_INFO_PROMPT = """You are a travel planning assistant analyzing user requests.

Extract structured information from the user's travel request:
- Travel dates (start and end)
- Budget amount (in KRW)
- Interests and preferences
- Number of travelers
- Special requirements

User request: {user_request}

Return a JSON object with:
{{
    "dates": ["YYYY-MM-DD", "YYYY-MM-DD"],
    "budget": <int>,
    "interests": [<list of strings>],
    "travelers": <int>,
    "special_requirements": [<list of strings>]
}}
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
1. Use ACTUAL dates from the travel period above (not YYYY-MM-DD placeholders)
2. Create day-by-day itinerary with specific times (HH:MM format)
3. Select venues from the provided lists above
4. Distribute budget reasonably across days
5. Consider typical opening hours (museums 10:00-18:00, restaurants 11:00-22:00)
6. Include breakfast, lunch, dinner for each day

IMPORTANT: Fill in the "date" field with real dates from the period {start_date} to {end_date}.
For example, if the trip is Jan 15-17:
- Day 1 date: "2025-01-15"
- Day 2 date: "2025-01-16"
- Day 3 date: "2025-01-17"

Return a JSON object with:
{{
    "title": "<plan title>",
    "total_days": <int>,
    "total_cost": <int>,
    "itinerary": [
        {{
            "day": 1,
            "date": "<ACTUAL DATE from travel period, e.g., 2025-01-15>",
            "theme": "<day theme>",
            "activities": [
                {{
                    "time": "HH:MM",
                    "venue_name": "<name from available venues>",
                    "venue_type": "attraction|restaurant|accommodation",
                    "duration_minutes": <int>,
                    "estimated_cost": <int>,
                    "notes": "<brief notes or tips>"
                }}
            ],
            "daily_cost": <int>
        }}
    ],
    "accommodation": {{
        "name": "<hotel name from available accommodations>",
        "cost_per_night": <int>,
        "total_nights": <int>
    }},
    "summary": "<brief plan summary>"
}}
"""

VALIDATE_PLAN_PROMPT = """Validate this travel plan for CRITICAL logical errors only:

Plan: {plan}
Budget: {budget:,} KRW

Check ONLY for these CRITICAL issues:
1. Time conflicts: Activities with overlapping time slots on the same day
2. Budget violations: Total cost exceeds budget by more than 20%
3. Missing dates: Any day missing the "date" field or using "YYYY-MM-DD" placeholder
4. Empty itinerary: No activities planned

DO NOT flag these as errors (they are acceptable):
- Missing detailed cost breakdowns (estimated costs are fine)
- Missing explicit travel time between venues (assume 10-30 min buffer)
- Opening hours not verified (assume typical business hours)
- Minor timing issues (5-10 minute overlaps are acceptable)

Return validation result as JSON:
{{
    "is_valid": true|false,
    "errors": [<list of CRITICAL error messages only>]
}}
"""
