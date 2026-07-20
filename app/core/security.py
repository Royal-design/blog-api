from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings
from app.core.exceptions import AppException
from app.models.enums import TokenType


password_hash = PasswordHash.recommended()
revoked_token_ids: set[str] = set()


# -------------------------
# PASSWORDS
# -------------------------
def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# -------------------------
# TOKEN CREATION
# -------------------------
def create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: TokenType,
) -> str:
    payload = data.copy()

    payload.update(
        {
            "exp": datetime.now(timezone.utc) + expires_delta,
            "type": token_type.value,
            "jti": str(uuid4()),
        }
    )

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_access_token(data: dict) -> str:
    return create_token(
        data,
        timedelta(minutes=settings.access_token_expire_minutes),
        TokenType.ACCESS,
    )


def create_refresh_token(data: dict) -> str:
    return create_token(
        data,
        timedelta(days=settings.refresh_token_expire_days),
        TokenType.REFRESH,
    )


def create_password_reset_token(data: dict) -> str:
    return create_token(
        data,
        timedelta(minutes=15),
        TokenType.PASSWORD_RESET,
    )


# -------------------------
# TOKEN DECODE (ONLY AppException)
# -------------------------
def decode_token(
    token: str,
    expected_type: TokenType | None = None,
) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        token_id = payload.get("jti")

        if token_id in revoked_token_ids:
            raise AppException(
                message="Token has been revoked",
                status_code=401,
                error_code="TOKEN_REVOKED",
            )

        if (
            expected_type is not None
            and payload.get("type") != expected_type.value
        ):
            raise AppException(
                message="Invalid token type",
                status_code=401,
                error_code="INVALID_TOKEN_TYPE",
            )

        return payload

    except ExpiredSignatureError:
        raise AppException(
            message="Token has expired",
            status_code=401,
            error_code="TOKEN_EXPIRED",
        )

    except InvalidTokenError:
        raise AppException(
            message="Invalid token",
            status_code=401,
            error_code="INVALID_TOKEN",
        )


# -------------------------
# HELPERS
# -------------------------
def decode_access_token(token: str) -> dict:
    return decode_token(token, TokenType.ACCESS)


def decode_refresh_token(token: str) -> dict:
    return decode_token(token, TokenType.REFRESH)


def decode_password_reset_token(token: str) -> dict:
    return decode_token(token, TokenType.PASSWORD_RESET)


def revoke_token(token: str) -> None:
    payload = decode_token(token)

    token_id = payload.get("jti")

    if token_id:
        revoked_token_ids.add(token_id)


def get_token_jti(token: str) -> str | None:
    return decode_token(token).get("jti")
