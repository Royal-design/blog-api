from uuid import UUID

from app.core.exceptions import AppException
from app.models.follow import Follow
from app.repositories.follow_repository import FollowRepository
from app.services.user_service import UserService


class FollowService:
    def __init__(
        self,
        follow_repository: FollowRepository,
        user_service: UserService,
    ):
        self.follow_repository = follow_repository
        self.user_service = user_service

    def get_followers(self, user_id: UUID):
        self.user_service.get_user_by_id(user_id)
        return self.follow_repository.get_followers(user_id)

    def get_following(self, user_id: UUID):
        self.user_service.get_user_by_id(user_id)
        return self.follow_repository.get_following(user_id)

    def follow_user(self, follower_id: UUID, following_id: UUID):
        if follower_id == following_id:
            raise AppException(message="You cannot follow yourself", status_code=400)

        self.user_service.get_user_by_id(following_id)

        existing = self.follow_repository.get_follow(follower_id, following_id)
        if existing:
            raise AppException(message="User already followed", status_code=400)

        return self.follow_repository.create_follow(
            Follow(follower_id=follower_id, following_id=following_id)
        )

    def unfollow_user(self, follower_id: UUID, following_id: UUID):
        follow = self.follow_repository.get_follow(follower_id, following_id)

        if not follow:
            raise AppException(message="Follow not found", status_code=404)

        return self.follow_repository.delete_follow(follow)
