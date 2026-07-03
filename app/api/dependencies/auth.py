from uuid import UUID

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.dependencies.services import get_user_service
from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.services.user_service import UserService
from app.models.user import User


bearer_scheme = HTTPBearer()


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> str:
    return credentials.credentials


def get_current_user(
    token: str = Depends(get_bearer_token),
    user_service: UserService = Depends(get_user_service),
) -> User:

    payload = decode_access_token(token)

    # 1. validate subject
    try:
        user_id = UUID(payload.get("sub"))
    except (AttributeError, TypeError, ValueError):
        raise AppException(
            message="Invalid token subject",
            status_code=401,
            error_code="INVALID_TOKEN",
        )

    # 2. fetch user
    user = user_service.get_user_by_id(user_id)

    if not user:
        raise AppException(
            message="User not found",
            status_code=404,
            error_code="USER_NOT_FOUND",
        )

    return user
