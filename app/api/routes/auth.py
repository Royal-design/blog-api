from fastapi import APIRouter, Body, Depends, BackgroundTasks, status

from app.api.dependencies.services import get_auth_service
from app.api.dependencies.auth import get_current_user, get_bearer_token

from app.schemas.auth import (
    AuthResponse,
    ForgotPasswordRequest,
    LogoutRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
)

from app.schemas.user import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    
)

from app.models.user import User
from app.services.auth_service import AuthService

from app.schemas.response import MessageResponse, SuccessResponse

router = APIRouter()


# -------------------------
# REGISTER
# -------------------------
@router.post(
    "/register",
    response_model=SuccessResponse[AuthResponse],
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: RegisterRequest,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(get_auth_service),
):
    auth_data = auth_service.register(user, background_tasks)

    return SuccessResponse(
        message="User registered successfully",
        data=AuthResponse.model_validate(auth_data)
    )


# -------------------------
# LOGIN
# -------------------------
@router.post("/login", response_model=AuthResponse)
def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.login(data)


# -------------------------
# REFRESH TOKEN
# -------------------------
@router.post("/refresh", response_model=AuthResponse)
def refresh(
    data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.refresh(data)


# -------------------------
# LOGOUT
# -------------------------
@router.post("/logout", response_model=MessageResponse)
def logout(
    logout_data: LogoutRequest | None = Body(default=None),
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.logout(
        access_token=token,
        refresh_token=logout_data.refresh_token if logout_data else None,
    )


# -------------------------
# FORGOT PASSWORD
# -------------------------
@router.post(
    "/forgot-password",
    response_model=MessageResponse
)
def forgot_password(
    data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.forgot_password(data, background_tasks)


# -------------------------
# RESET PASSWORD
# -------------------------
@router.post(
    "/reset-password",
    response_model=MessageResponse
)
def reset_password(
    data: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.reset_password(data)


# -------------------------
# CHANGE PASSWORD
# -------------------------
@router.post(
    "/change-password",
    response_model=MessageResponse
)
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.change_password(
        user_id=current_user.id,
        request=data,
    )
