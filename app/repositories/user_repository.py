from sqlalchemy.orm import  Session

from app.models.user import User

class User_Repository:
    def __init__(self, db:Session):
        self.db = db

    def get_user_by_id(self, user_id: str)-> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str)-> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_all(self)-> list[User]:
        return self.db.query(User).all()

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