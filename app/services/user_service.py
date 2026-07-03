from uuid import UUID

from app.core.exceptions import AppException
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import RegisterRequest, UserUpdateRequest


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    # -------------------------
    # GET ALL USERS
    # -------------------------
    def get_all_users(self) -> list[User]:
        return self.repository.get_user_all()

    # -------------------------
    # GET USER BY ID
    # -------------------------
    def get_user_by_id(self, user_id: UUID) -> User:
        user = self.repository.get_user_by_id(user_id)

        if not user:
            raise AppException(
                message="User not found",
                status_code=404,
                error_code="USER_NOT_FOUND",
            )

        return user

    # -------------------------
    # GET USER BY EMAIL
    # -------------------------
    def get_user_by_email(self, email: str) -> User | None:
        return self.repository.get_user_by_email(email)
    
    
    # -------------------------
    # GET USER BY USERNAME
    # -------------------------
    
    def get_user_by_username(self, username: str):
        return self.repository.get_user_by_username(username)

    # -------------------------
    # CREATE USER
    # -------------------------
    def create_user(
        self,
        user: RegisterRequest,
        hashed_password: str,
    ) -> User:

        if self.get_user_by_email(user.email):
            raise AppException(
                message="Email already exists",
                status_code=409,
                error_code="EMAIL_ALREADY_EXISTS",
            )

        if self.get_user_by_username(user.username):
            raise AppException(
                message="Username already exists",
                status_code=409,
                error_code="USERNAME_ALREADY_EXISTS",
            )

        db_user = User(
            **user.model_dump(exclude={"password"}),
            password=hashed_password,
        )

        return self.repository.create_user(db_user)

    # -------------------------
    # UPDATE USER
    # -------------------------
    def update_user(
        self,
        user_id: UUID,
        user: UserUpdateRequest,
    ) -> User:

        db_user = self.get_user_by_id(user_id)

        updates = user.model_dump(exclude_unset=True)

        if "email" in updates:
            existing_user = self.get_user_by_email(updates["email"])

            if existing_user and existing_user.id != user_id:
                raise AppException(
                    message="Email already exists",
                    status_code=409,
                    error_code="EMAIL_ALREADY_EXISTS",
                )
        if "username" in updates:
            existing_user = self.get_user_by_username(updates["username"])

            if existing_user and existing_user.id != user_id:
                raise AppException(
                    message="Username already exists",
                    status_code=409,
                    error_code="USERNAME_ALREADY_EXISTS",
                )

        if "password" in updates:
            updates["password"] = hash_password(updates["password"])

        for key, value in updates.items():
            setattr(db_user, key, value)

        return self.repository.update_user(db_user)

    # -------------------------
    # DELETE USER
    # -------------------------
    def delete_user(self, user_id: UUID) -> User:

        user = self.get_user_by_id(user_id)

        return self.repository.delete_user(user)
