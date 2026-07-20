from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    content: str
    post_id: UUID
    parent_id: UUID | None = None


class CommentUpdate(BaseModel):
    content: str


class CommentUserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(BaseModel):
    id: UUID
    content: str
    user_id: UUID
    post_id: UUID
    parent_id: UUID | None
    created_at: datetime
    updated_at: datetime
    user: CommentUserResponse

    model_config = ConfigDict(from_attributes=True)
