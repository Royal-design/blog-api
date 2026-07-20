from datetime import datetime, timezone

from fastapi import BackgroundTasks
from uuid import UUID

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.security import (
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    decode_password_reset_token,
    decode_refresh_token,
    get_token_jti,
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
    RegisterRequest,
    LoginRequest,
)
from app.services.email_service import EmailService
from app.services.refresh_token_service import RefreshTokenService
from app.services.user_service import UserService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        email_service: EmailService,
        refresh_token_service: RefreshTokenService,
    ):
        self.user_service = user_service
        self.email_service = email_service
        self.refresh_token_service = refresh_token_service

    # -------------------------
    # REGISTER
    # -------------------------
    def register(
        self,
        user: RegisterRequest,
        background_tasks: BackgroundTasks,
    ):
        hashed_password = hash_password(user.password)

        db_user = self.user_service.create_user(
            user,
            hashed_password,
        )

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
    def login(self, login_data: LoginRequest):
        user = self.user_service.get_user_by_email(
            login_data.email
        )

        if not user:
            raise AppException(
                message="Invalid credentials",
                status_code=401,
                error_code="INVALID_CREDENTIALS",
            )

        if not verify_password(
            login_data.password,
            user.password,
        ):
            raise AppException(
                message="Invalid credentials",
                status_code=401,
                error_code="INVALID_CREDENTIALS",
            )

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

        token_jti = payload.get("jti")
        if not token_jti:
            raise AppException(
                message="Invalid refresh token",
                status_code=401,
                error_code="INVALID_REFRESH_TOKEN",
            )

        self.refresh_token_service.validate_refresh_token(token_jti)

        try:
            user_id = UUID(payload["sub"])
        except (KeyError, TypeError, ValueError):
            raise AppException(
                message="Invalid token subject",
                status_code=401,
                error_code="INVALID_TOKEN",
            )

        user = self.user_service.get_user_by_id(user_id)

        self.refresh_token_service.revoke_refresh_token(token_jti)
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
            token_jti = get_token_jti(refresh_token)
            if token_jti:
                self.refresh_token_service.revoke_refresh_token(token_jti)
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
            f"{settings.frontend_url}/reset-password?token={reset_token}"
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
            user_id = UUID(payload["sub"])
        except (KeyError, TypeError, ValueError):
            raise AppException(
                message="Invalid reset token",
                status_code=401,
                error_code="INVALID_RESET_TOKEN",
            )

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
        user_id: UUID,
        request: ChangePasswordRequest,
    ):
        user = self.user_service.get_user_by_id(user_id)

        if not verify_password(
            request.current_password,
            user.password,
        ):
            raise AppException(
                message="Current password is incorrect",
                status_code=401,
                error_code="INVALID_PASSWORD",
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

        refresh_token = create_refresh_token(payload)
        refresh_payload = decode_refresh_token(refresh_token)
        expires_at = datetime.fromtimestamp(
            refresh_payload["exp"],
            tz=timezone.utc,
        )

        self.refresh_token_service.store_refresh_token(
            token_jti=refresh_payload["jti"],
            user_id=user.id,
            expires_at=expires_at,
        )

        return {
            "access_token": create_access_token(payload),
            "refresh_token": refresh_token,
        }
