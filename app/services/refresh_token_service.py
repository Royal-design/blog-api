from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import AppException
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository


class RefreshTokenService:
    def __init__(self, refresh_token_repository: RefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository

    def store_refresh_token(
        self,
        token_jti: str,
        user_id: UUID,
        expires_at: datetime,
    ):
        refresh_token = RefreshToken(
            token_jti=token_jti,
            user_id=user_id,
            expires_at=expires_at,
        )
        return self.refresh_token_repository.create_refresh_token(refresh_token)

    def validate_refresh_token(self, token_jti: str):
        refresh_token = self.refresh_token_repository.get_by_jti(token_jti)

        if not refresh_token:
            raise AppException(
                message="Refresh token not found",
                status_code=401,
                error_code="INVALID_REFRESH_TOKEN",
            )

        if refresh_token.revoked:
            raise AppException(
                message="Refresh token has been revoked",
                status_code=401,
                error_code="TOKEN_REVOKED",
            )

        expires_at = refresh_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= datetime.now(timezone.utc):
            raise AppException(
                message="Refresh token has expired",
                status_code=401,
                error_code="TOKEN_EXPIRED",
            )

        return refresh_token

    def revoke_refresh_token(self, token_jti: str):
        return self.refresh_token_repository.revoke_by_jti(token_jti)
