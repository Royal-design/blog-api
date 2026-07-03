from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import AuthProvider, UserRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    bio: str | None = None
    avatar: str | None = None
    
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