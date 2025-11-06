"""Reviewer agent prompts."""

PARSE_FEEDBACK_PROMPT = """Analyze user feedback on a travel plan.

Original Plan: {original_plan}
User Feedback: {user_feedback}

Determine:
1. Feedback type: "approve" (satisfied), "reject" (start over), or "modify" (specific changes)
2. If modify, identify target section: day_1, day_2, budget, accommodation, etc.
3. Extract specific modification requests

Return JSON:
{{
    "feedback_type": "approve|reject|modify",
    "target_section": "<section>",
    "modification_requests": [<list of specific changes>],
    "reasoning": "<explanation>"
}}
"""

MODIFY_PLAN_PROMPT = """Modify the travel plan based on user feedback.

Original Plan: {original_plan}
Feedback Type: {feedback_type}
Target Section: {target_section}
Modification Requests: {modification_requests}

Guidelines:
1. Preserve unchanged sections exactly
2. Only modify the target section
3. Maintain budget and time constraints
4. Keep the overall plan structure consistent
5. Ensure modified section flows with rest of plan

Return the COMPLETE modified plan in the same JSON structure as the original.
"""
