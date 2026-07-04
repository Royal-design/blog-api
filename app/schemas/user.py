from datetime import datetime
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import AuthProvider, UserRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    bio: str | None = None
    avatar: str | None = None
    avatar_public_id: str | None = None
    
class RegisterRequest(UserBase):
    password: str
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class UserUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    bio: str | None = None
    avatar: str | None = None
    avatar_public_id: str | None = None
    
class UserResponse(UserBase):
    id: UUID
    role: UserRole
    provider: AuthProvider
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        min_length=10,
        description="JWT refresh token"
    )

class UserProfileRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    bio: str | None = None
  
    
    @classmethod
    def get_form(
        cls,
        first_name: str | None = Form(None),
        last_name: str | None = Form(None),
        username: str | None = Form(None),
        bio: str | None = Form(None)
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            username=username,
            bio=bio
        )