"""Auth domain router."""

from fastapi import APIRouter
from .schemas import UserCreate, UserLogin, Token, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Register a new user."""
    # TODO: Implement user registration
    return UserResponse(id=1, email=user.email, full_name=user.full_name)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login and get access token."""
    # TODO: Implement login logic
    return Token(access_token="dummy-token-for-testing")


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current authenticated user."""
    # TODO: Implement current user retrieval
    return UserResponse(id=1, email="test@example.com", full_name="Test User")
