"""
DEPRECATED: This file has been migrated to domain-based structure.

Tests have been moved to:
- tests/unit/auth/test_user_models.py (User model tests)
- tests/unit/plan/test_plan_models.py (TravelPlan model tests)
- tests/unit/tourist_attraction/test_attraction_models.py (TouristAttraction model tests)

This file is kept for backwards compatibility but will be removed in future versions.
"""

# Import all tests from new locations for backwards compatibility
from tests.unit.auth.test_user_models import TestUserModel
from tests.unit.plan.test_plan_models import TestTravelPlanModel
from tests.unit.tourist_attraction.test_attraction_models import TestTouristAttractionModel

__all__ = ["TestUserModel", "TestTravelPlanModel", "TestTouristAttractionModel"]
