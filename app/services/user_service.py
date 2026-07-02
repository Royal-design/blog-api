from app.core.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import User_Repository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: User_Repository):
        self.repository = repository

    def get_all_users(self) -> list[User]:
        return self.repository.get_user_all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repository.get_user_by_id(user_id)

        if not user:
            raise UserNotFoundError("User not found")

        return user

    def get_user_by_email(self, email: str) -> User | None:
        return self.repository.get_user_by_email(email)

    def create_user(
        self,
        user: UserCreate,
        hashed_password: str,
    ) -> User:
        if self.get_user_by_email(user.email):
            raise EmailAlreadyExistsError("Email already exists")

        db_user = User(
            **user.model_dump(exclude={"password"}),
            password=hashed_password,
        )

        return self.repository.create_user(db_user)

    def update_user(
        self,
        user_id: int,
        user: UserUpdate,
    ) -> User:
        db_user = self.get_user_by_id(user_id)

        updates = user.model_dump(exclude_unset=True)

        if "email" in updates:
            existing_user = self.get_user_by_email(updates["email"])

            if existing_user and existing_user.id != user_id:
                raise EmailAlreadyExistsError("Email already exists")

        if "password" in updates:
            updates["password"] = hash_password(updates["password"])

        for key, value in updates.items():
            setattr(db_user, key, value)

        return self.repository.update_user(db_user)

    def delete_user(self, user_id: int) -> User:
        user = self.get_user_by_id(user_id)

        return self.repository.delete_user(user)