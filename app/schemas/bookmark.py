from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.post import PostResponse


class BookmarkResponse(BaseModel):
    user_id: UUID
    post_id: UUID

    model_config = ConfigDict(from_attributes=True)


class BookmarkedPostResponse(BookmarkResponse):
    post: PostResponse
