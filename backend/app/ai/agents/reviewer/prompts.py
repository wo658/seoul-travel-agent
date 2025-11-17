"""Reviewer agent prompts."""

PARSE_FEEDBACK_PROMPT = """Analyze user feedback on a travel plan and determine what needs to be modified.

Original Plan: {original_plan}
User Feedback: {user_feedback}

Analyze and determine:
1. **Feedback type**:
   - "approve": User is satisfied with the plan
   - "reject": User wants to start over completely
   - "modify": User wants specific changes

2. **Target section** (if modifying): Which part to modify
   - Examples: "day_1", "day_2", "budget", "accommodation"

3. **Modification type** (if modifying): What category of change is needed
   - "restaurant", "food", or "meal": User wants different dining options
   - "attraction" or "activity": User wants different tourist spots or activities
   - "accommodation" or "hotel": User wants different lodging
   - "budget": User wants budget adjustments
   - "time": User wants schedule/timing changes
   - "general": Other modifications

4. **Reasoning**: Explain your analysis of the feedback

Examples:
- "첫째 날 점심을 덜 비싼 곳으로 바꿔줘" → modification_type: "restaurant"
- "더 재미있는 관광지로 바꿔줘" → modification_type: "attraction"
- "더 좋은 호텔로 바꿔줘" → modification_type: "accommodation"
- "예산을 50만원으로 줄여줘" → modification_type: "budget"
"""

MODIFY_PLAN_PROMPT = """Modify the travel plan based on user feedback using the provided context data.

**Original Plan:**
{original_plan}

**User Feedback:** {user_feedback}

**Modification Type:** {modification_type}

**Target Section:** {target_section}

**Available Context Data (use this for modifications):**
{context_data}

**Guidelines:**
1. **Use context data**: If restaurants/attractions/accommodations are provided, SELECT appropriate options from this data
   - IMPORTANT: Choose from the provided options rather than inventing new venues
2. **Preserve structure**: Keep unchanged sections exactly as they are
3. **Maintain constraints**: Ensure budget and time constraints are met
4. **Consistency**: Modified section must flow naturally with the rest of the plan
5. **Complete response**: Return the COMPLETE modified plan with all fields filled in
6. **Match original structure**: The output should have the same structure as the original plan
   - Include: title, total_days, total_cost, itinerary (with daily activities), accommodation, summary

Return the complete modified travel plan maintaining all the structure and fields from the original.
"""
