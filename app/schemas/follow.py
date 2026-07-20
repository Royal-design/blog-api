from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserResponse


class FollowResponse(BaseModel):
    follower_id: UUID
    following_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FollowerResponse(FollowResponse):
    follower: UserResponse


class FollowingResponse(FollowResponse):
    following: UserResponse
