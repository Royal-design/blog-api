from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.comment import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def _query_with_relationships(self):
        return self.db.query(Comment).options(selectinload(Comment.user))

    def get_all_comments(self):
        return self._query_with_relationships().all()

    def get_comments_by_post_id(self, post_id: UUID):
        return (
            self._query_with_relationships()
            .filter(Comment.post_id == post_id)
            .order_by(Comment.created_at.asc())
            .all()
        )

    def get_comment_by_id(self, comment_id: UUID):
        return self._query_with_relationships().filter(Comment.id == comment_id).first()

    def create_comment(self, comment: Comment):
        self.db.add(comment)
        self.db.commit()
        return self.get_comment_by_id(comment.id)

    def update_comment(self, comment: Comment):
        self.db.commit()
        return self.get_comment_by_id(comment.id)

    def delete_comment(self, comment: Comment):
        self.db.delete(comment)
        self.db.commit()
        return comment
