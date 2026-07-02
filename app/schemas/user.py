from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import AuthProvider, UserRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    bio: str | None = None
    avatar: str | None = None
    
class UserCreate(UserBase):
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserUpdate(BaseModel):
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