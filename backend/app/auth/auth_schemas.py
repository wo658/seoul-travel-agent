"""Auth domain schemas."""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """User creation schema."""

    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    """User login schema."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    email: str
    full_name: str

    class Config:
        from_attributes = True
