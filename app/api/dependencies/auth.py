from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.dependencies.services import get_user_service
from app.core.exceptions import InvalidTokenException
from app.core.security import decode_access_token
from app.models.user import User
from app.services.user_service import UserService



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

    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError):
        raise InvalidTokenException("Invalid token")

    return user_service.get_user_by_id(user_id)