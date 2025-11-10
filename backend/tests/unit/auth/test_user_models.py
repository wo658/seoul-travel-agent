"""Test Auth domain models."""

import pytest


class TestUserModel:
    """Test User model."""

    def test_create_user(self, test_db_session):
        """Test creating a user."""
        from app.auth.models import User

        user = User(
            email="unique_test@example.com",
            username="uniquetestuser",
            hashed_password="hashed_password_here",
        )
        test_db_session.add(user)
        test_db_session.commit()
        test_db_session.refresh(user)

        assert user.id is not None
        assert user.email == "unique_test@example.com"
        assert user.username == "uniquetestuser"
        # SQLite stores boolean as integer (1 for True)
        assert user.is_active == 1
        assert user.created_at is not None

    def test_user_relationships(self, test_db_session, mock_user, mock_travel_plan):
        """Test user relationships with travel plans."""
        assert len(mock_user.plans) == 1
        assert mock_user.plans[0].id == mock_travel_plan.id
