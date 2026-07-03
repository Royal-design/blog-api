from sqlalchemy.orm import Session

from app.core.exceptions import InvalidCredentialsError, InvalidTokenException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    revoke_token,
    verify_password,
)
from app.schemas.user import RefreshTokenRequest, UserCreate, UserInLogin
from app.services.user_service import UserService


class AuthService:
    def __init__(self, user_service:UserService):
        self.user_service = user_service

    def register(self, user: UserCreate):
        hashed_password = hash_password(user.password)

        db_user = self.user_service.create_user(
            user,
            hashed_password,
        )

        tokens = self._create_auth_tokens(db_user)

        return {
            "user": db_user,
            **tokens,
            "token_type": "bearer",
        }

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

    def refresh(self, refresh_data: RefreshTokenRequest):
        payload = decode_refresh_token(refresh_data.refresh_token)
        user_id = payload.get("sub")

        if not user_id:
            raise InvalidTokenException("Invalid token subject")

        try:
            user = self.user_service.get_user_by_id(int(user_id))
        except ValueError:
            raise InvalidTokenException("Invalid token subject")

        tokens = self._create_auth_tokens(user)

        revoke_token(refresh_data.refresh_token)

        return {
            "user": user,
            **tokens,
            "token_type": "bearer",
        }

    def logout(self, access_token: str, refresh_token: str | None = None):
        revoke_token(access_token)

        if refresh_token:
            revoke_token(refresh_token)

        return {"message": "User logged out successfully"}

    def _create_auth_tokens(self, user):
        payload = {
            "sub": str(user.id),
            "email": user.email,
        }

        return {
            "access_token": create_access_token(payload),
            "refresh_token": create_refresh_token(payload),
        }
