from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.post import PostResponse


class LikeResponse(BaseModel):
    user_id: UUID
    post_id: UUID

    model_config = ConfigDict(from_attributes=True)


class LikedPostResponse(LikeResponse):
    post: PostResponse
