from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService



def get_user_service(db:Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)

def get_auth_service(user_service:UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(user_service)