from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import  Session

from app.models.user import User

class UserRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_user_by_id(self, user_id: UUID)-> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str)-> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str)-> User | None:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_all(
        self,
        search: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[User], int]:

        query = self.db.query(User)

        # -------------------------
        # SEARCH FILTER
        # -------------------------
        if search:
            query = query.filter(
                or_(
                    User.first_name.ilike(f"%{search}%"),
                    User.last_name.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )

        # -------------------------
        # TOTAL COUNT (before pagination)
        # -------------------------
        total = query.count()

        # -------------------------
        # PAGINATION
        # -------------------------
        offset = (page - 1) * page_size

        users = (
            query
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return users, total

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user:User):
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user:User):
        self.db.delete(user)
        self.db.commit()
        return user
