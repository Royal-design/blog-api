from uuid import UUID

from fastapi import UploadFile

from app.core.exceptions import AppException
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import RegisterRequest, UserProfileRequest, UserUpdateRequest
from app.services.cloudinary_service import CloudinaryService


class UserService:
    def __init__(self, repository: UserRepository, cloudinary:CloudinaryService):
        self.repository = repository
        self.cloudinary = cloudinary

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
    # UPDATE USER PROFILE
    # -------------------------
    
    def update_profile(
    self,
    user_id: UUID,
    request: UserProfileRequest,
    avatar: UploadFile | None = None,
) -> User:

        user = self.get_user_by_id(user_id)

        updates = request.model_dump(exclude_unset=True)

        if "username" in updates:
            existing = self.get_user_by_username(updates["username"])

            if existing and existing.id != user.id:
                raise AppException(
                    message="Username already exists",
                    status_code=409,
                    error_code="USERNAME_ALREADY_EXISTS",
                )

        for key, value in updates.items():
            setattr(user, key, value)

        if avatar:
            if user.avatar_public_id:
                self.cloudinary.delete_image(user.avatar_public_id)

            image = self.cloudinary.upload_image(
                avatar,
                folder="blog/avatars",
            )

            user.avatar = image["url"]
            user.avatar_public_id = image["public_id"]

        return self.repository.update_user(user)

    # -------------------------
    # DELETE USER
    # -------------------------
    
    def delete_user(self, user_id: UUID) -> User:
        if not user_id:
            raise AppException(
                message="User id is required",
                status_code=400,
                error_code="INVALID_USER_ID",
            )

        user = self.get_user_by_id(user_id)

        return self.repository.delete_user(user)
