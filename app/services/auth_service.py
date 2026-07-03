from fastapi import BackgroundTasks

from app.core.config import settings
from app.core.exceptions import (
    InvalidCredentialsError,
    InvalidTokenException,
)
from app.core.security import (
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    decode_password_reset_token,
    decode_refresh_token,
    hash_password,
    revoke_token,
    verify_password,
)
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.response import MessageResponse
from app.schemas.user import (
    RefreshTokenRequest,
    UserCreate,
    UserInLogin,
)
from app.services.email_service import EmailService
from app.services.user_service import UserService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        email_service: EmailService,
    ):
        self.user_service = user_service
        self.email_service = email_service

    # -------------------------
    # REGISTER
    # -------------------------
    def register(
        self,
        user: UserCreate,
        background_tasks: BackgroundTasks,
    ):
        hashed_password = hash_password(user.password)

        db_user = self.user_service.create_user(
            user,
            hashed_password,
        )

        # send welcome email (non-blocking)
        background_tasks.add_task(
            self.email_service.send_welcome_email,
            db_user.email,
            db_user.first_name,
        )

        tokens = self._create_auth_tokens(db_user)

        return {
            "user": db_user,
            **tokens,
            "token_type": "bearer",
        }

    # -------------------------
    # LOGIN
    # -------------------------
    def login(self, login_data: UserInLogin):
        user = self.user_service.get_user_by_email(
            login_data.email
        )

        if not user:
            raise InvalidCredentialsError()

        if not verify_password(
            login_data.password,
            user.password,
        ):
            raise InvalidCredentialsError()

        tokens = self._create_auth_tokens(user)

        return {
            "user": user,
            **tokens,
            "token_type": "bearer",
        }

    # -------------------------
    # REFRESH TOKEN
    # -------------------------
    def refresh(self, refresh_data: RefreshTokenRequest):
        payload = decode_refresh_token(
            refresh_data.refresh_token
        )

        try:
            user_id = int(payload["sub"])
        except (KeyError, TypeError, ValueError):
            raise InvalidTokenException("Invalid token subject")

        user = self.user_service.get_user_by_id(user_id)

        revoke_token(refresh_data.refresh_token)

        tokens = self._create_auth_tokens(user)

        return {
            "user": user,
            **tokens,
            "token_type": "bearer",
        }

    # -------------------------
    # LOGOUT
    # -------------------------
    def logout(
        self,
        access_token: str,
        refresh_token: str | None = None,
    ):
        revoke_token(access_token)

        if refresh_token:
            revoke_token(refresh_token)

        return MessageResponse(
            message="Successfully logged out",
        )

    # -------------------------
    # FORGOT PASSWORD
    # -------------------------
    def forgot_password(
        self,
        request: ForgotPasswordRequest,
        background_tasks: BackgroundTasks,
    ):
        user = self.user_service.get_user_by_email(
            request.email
        )

        # always return same response (security best practice)
        response = MessageResponse(
            message=(
                "If an account exists with this email, "
                "a reset link has been sent."
            )
        )

        if not user:
            return response

        reset_token = create_password_reset_token(
            {"sub": str(user.id)}
        )

        reset_link = (
            f"{settings.frontend_url}"
            f"/reset-password?token={reset_token}"
        )

        background_tasks.add_task(
            self.email_service.send_password_reset_email,
            user.email,
            reset_link,
        )

        return response

    # -------------------------
    # RESET PASSWORD
    # -------------------------
    def reset_password(
        self,
        request: ResetPasswordRequest,
    ):
        payload = decode_password_reset_token(
            request.token
        )

        try:
            user_id = int(payload["sub"])
        except (KeyError, TypeError, ValueError):
            raise InvalidTokenException("Invalid reset token")

        user = self.user_service.get_user_by_id(user_id)

        user.password = hash_password(
            request.new_password
        )

        self.user_service.save_user(user)

        revoke_token(request.token)

        return MessageResponse(
            message="Password reset successfully",
        )

    # -------------------------
    # CHANGE PASSWORD
    # -------------------------
    def change_password(
        self,
        user_id: int,
        request: ChangePasswordRequest,
    ):
        user = self.user_service.get_user_by_id(user_id)

        if not verify_password(
            request.current_password,
            user.password,
        ):
            raise InvalidCredentialsError(
                "Current password is incorrect"
            )

        user.password = hash_password(
            request.new_password
        )

        self.user_service.save_user(user)

        return MessageResponse(
            message="Password changed successfully",
        )

    # -------------------------
    # TOKENS
    # -------------------------
    def _create_auth_tokens(self, user):
        payload = {
            "sub": str(user.id),
            "email": user.email,
        }

        return {
            "access_token": create_access_token(payload),
            "refresh_token": create_refresh_token(payload),
        }