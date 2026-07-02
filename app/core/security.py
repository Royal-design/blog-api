from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
from pwdlib import PasswordHash

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)
from app.core.exceptions import InvalidCredentialsError, InvalidTokenException

password_hash = PasswordHash.recommended()
revoked_token_ids: set[str] = set()

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(password:str, hashed_password:str)-> bool:
    return password_hash.verify(password, hashed_password)

def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    payload["exp"] = expire
    payload["type"] = token_type
    payload["jti"] = str(uuid4())

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )   


def create_access_token(data: dict) -> str:
    return create_token(
        data,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "access",
    )


def create_refresh_token(data: dict) -> str:
    return create_token(
        data,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "refresh",
    )


def decode_token(token: str, expected_type: str | None = None) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        token_id = payload.get("jti")
        if token_id in revoked_token_ids:
            raise InvalidTokenException("Token has been revoked")

        if expected_type and payload.get("type") != expected_type:
            raise InvalidTokenException("Invalid token type")

        return payload
    except ExpiredSignatureError:
        raise InvalidCredentialsError("Token has expired")
    except InvalidTokenError:
        raise InvalidTokenException("Invalid token")


def decode_access_token(token: str) -> dict:
    return decode_token(token, "access")


def decode_refresh_token(token: str) -> dict:
    return decode_token(token, "refresh")


def revoke_token(token: str) -> None:
    payload = decode_token(token)
    token_id = payload.get("jti")
    if token_id:
        revoked_token_ids.add(token_id)
