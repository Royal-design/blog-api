from uuid import UUID

from app.core.exceptions import AppException
from app.models.like import Like
from app.repositories.like_repository import LikeRepository
from app.services.post_service import PostService


class LikeService:
    def __init__(
        self,
        like_repository: LikeRepository,
        post_service: PostService,
    ):
        self.like_repository = like_repository
        self.post_service = post_service

    def get_my_likes(self, user_id: UUID):
        return self.like_repository.get_likes_by_user_id(user_id)

    def like_post(self, user_id: UUID, post_id: UUID):
        self.post_service.get_post_by_id(post_id)

        existing = self.like_repository.get_like(user_id, post_id)
        if existing:
            raise AppException(message="Post already liked", status_code=400)

        return self.like_repository.create_like(
            Like(user_id=user_id, post_id=post_id)
        )

    def unlike_post(self, user_id: UUID, post_id: UUID):
        like = self.like_repository.get_like(user_id, post_id)

        if not like:
            raise AppException(message="Like not found", status_code=404)

        return self.like_repository.delete_like(like)
