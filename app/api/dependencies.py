from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import InvalidTokenException
from app.core.security import decode_access_token
from app.models.user import User
from app.services.user_service import UserService


bearer_scheme = HTTPBearer(scheme_name="Bearer")


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> str:
    return credentials.credentials


def get_current_user(
    token: str = Depends(get_bearer_token),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise InvalidTokenException("Invalid token subject")

    try:
        return UserService(db).get_user_by_id(int(user_id))
    except ValueError:
        raise InvalidTokenException("Invalid token subject")
