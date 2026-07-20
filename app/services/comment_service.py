from uuid import UUID

from app.core.exceptions import AppException
from app.models.comment import Comment
from app.models.user import User
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.post_service import PostService


class CommentService:
    def __init__(
        self,
        comment_repository: CommentRepository,
        post_service: PostService,
    ):
        self.comment_repository = comment_repository
        self.post_service = post_service

    def get_all_comments(self):
        return self.comment_repository.get_all_comments()

    def get_comments_by_post_id(self, post_id: UUID):
        self.post_service.get_post_by_id(post_id)
        return self.comment_repository.get_comments_by_post_id(post_id)

    def get_comment_by_id(self, comment_id: UUID):
        comment = self.comment_repository.get_comment_by_id(comment_id)

        if not comment:
            raise AppException(message="Comment not found", status_code=404)

        return comment

    def create_comment(self, request: CommentCreate, current_user: User):
        self.post_service.get_post_by_id(request.post_id)

        if request.parent_id:
            parent = self.get_comment_by_id(request.parent_id)
            if parent.post_id != request.post_id:
                raise AppException(
                    message="Parent comment must belong to the same post",
                    status_code=400,
                )

        comment = Comment(
            content=request.content,
            user_id=current_user.id,
            post_id=request.post_id,
            parent_id=request.parent_id,
        )

        return self.comment_repository.create_comment(comment)

    def update_comment(
        self,
        comment_id: UUID,
        request: CommentUpdate,
        current_user: User,
    ):
        comment = self.get_comment_by_id(comment_id)
        self._check_comment_permission(comment, current_user)

        comment.content = request.content
        return self.comment_repository.update_comment(comment)

    def delete_comment(self, comment_id: UUID, current_user: User):
        comment = self.get_comment_by_id(comment_id)
        self._check_comment_permission(comment, current_user)
        return self.comment_repository.delete_comment(comment)

    def _check_comment_permission(self, comment: Comment, current_user: User):
        if comment.user_id != current_user.id:
            raise AppException(
                message="You are not authorized to perform this action",
                status_code=403,
            )
