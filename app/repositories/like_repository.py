from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.like import Like


class LikeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_like(self, user_id: UUID, post_id: UUID):
        return (
            self.db.query(Like)
            .filter(Like.user_id == user_id, Like.post_id == post_id)
            .first()
        )

    def get_likes_by_user_id(self, user_id: UUID):
        return (
            self.db.query(Like)
            .options(
                selectinload(Like.post),
                selectinload(Like.post).selectinload("author"),
                selectinload(Like.post).selectinload("category"),
                selectinload(Like.post).selectinload("tags"),
                selectinload(Like.post).selectinload("images"),
            )
            .filter(Like.user_id == user_id)
            .all()
        )

    def create_like(self, like: Like):
        self.db.add(like)
        self.db.commit()
        self.db.refresh(like)
        return like

    def delete_like(self, like: Like):
        self.db.delete(like)
        self.db.commit()
        return like
