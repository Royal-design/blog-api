from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.follow import Follow


class FollowRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_follow(self, follower_id: UUID, following_id: UUID):
        return (
            self.db.query(Follow)
            .filter(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
            )
            .first()
        )

    def get_followers(self, user_id: UUID):
        return (
            self.db.query(Follow)
            .options(selectinload(Follow.follower))
            .filter(Follow.following_id == user_id)
            .all()
        )

    def get_following(self, user_id: UUID):
        return (
            self.db.query(Follow)
            .options(selectinload(Follow.following))
            .filter(Follow.follower_id == user_id)
            .all()
        )

    def create_follow(self, follow: Follow):
        self.db.add(follow)
        self.db.commit()
        self.db.refresh(follow)
        return follow

    def delete_follow(self, follow: Follow):
        self.db.delete(follow)
        self.db.commit()
        return follow
