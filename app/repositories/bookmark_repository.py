from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.bookmark import Bookmark


class BookmarkRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_bookmark(self, user_id: UUID, post_id: UUID):
        return (
            self.db.query(Bookmark)
            .filter(Bookmark.user_id == user_id, Bookmark.post_id == post_id)
            .first()
        )

    def get_bookmarks_by_user_id(self, user_id: UUID):
        return (
            self.db.query(Bookmark)
            .options(
                selectinload(Bookmark.post),
                selectinload(Bookmark.post).selectinload("author"),
                selectinload(Bookmark.post).selectinload("category"),
                selectinload(Bookmark.post).selectinload("tags"),
                selectinload(Bookmark.post).selectinload("images"),
            )
            .filter(Bookmark.user_id == user_id)
            .all()
        )

    def create_bookmark(self, bookmark: Bookmark):
        self.db.add(bookmark)
        self.db.commit()
        self.db.refresh(bookmark)
        return bookmark

    def delete_bookmark(self, bookmark: Bookmark):
        self.db.delete(bookmark)
        self.db.commit()
        return bookmark
