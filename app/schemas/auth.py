from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserResponse


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(
        min_length=8,
        max_length=128,
        description="New password",
    )


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(
        min_length=8,
        max_length=128,
        description="New password",
    )


class LogoutRequest(BaseModel):
    refresh_token: str | None = Field(
        default=None,
        min_length=10,
        description="JWT refresh token",
    )


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
