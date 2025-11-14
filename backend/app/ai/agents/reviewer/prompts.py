"""Reviewer agent prompts."""

PARSE_FEEDBACK_PROMPT = """Analyze user feedback on a travel plan and determine what needs to be modified.

Original Plan: {original_plan}
User Feedback: {user_feedback}

Determine:
1. **Feedback type**: "approve" (satisfied), "reject" (start over), or "modify" (specific changes)
2. **Target section**: Which part to modify (e.g., "day_1", "day_2", "budget", "accommodation")
3. **Modification type**: What category of change is needed:
   - "restaurant" or "food" or "meal": User wants different dining options
   - "attraction" or "activity": User wants different tourist spots or activities
   - "accommodation" or "hotel": User wants different lodging
   - "budget": User wants budget adjustments
   - "time": User wants schedule/timing changes
   - "general": Other modifications

Examples:
- "첫째 날 점심을 덜 비싼 곳으로 바꿔줘" → modification_type: "restaurant"
- "더 재미있는 관광지로 바꿔줘" → modification_type: "attraction"
- "더 좋은 호텔로 바꿔줘" → modification_type: "accommodation"
- "예산을 50만원으로 줄여줘" → modification_type: "budget"

Return JSON:
{{
    "feedback_type": "approve|reject|modify",
    "target_section": "<section>",
    "modification_type": "restaurant|attraction|accommodation|budget|time|general",
    "reasoning": "<explanation>"
}}
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
2. **Preserve structure**: Keep unchanged sections exactly as they are
3. **Maintain constraints**: Ensure budget and time constraints are met
4. **Consistency**: Modified section must flow naturally with the rest of the plan
5. **Complete response**: Return the COMPLETE modified plan (not just the changed part)

**Important:** If context data contains relevant options (e.g., restaurants for restaurant modifications),
you MUST choose from these options rather than inventing new ones.

Return the COMPLETE modified plan in the same JSON structure as the original.
"""
