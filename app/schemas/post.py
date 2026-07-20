from datetime import datetime
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.models.enums import PostStatus


class PostBase(BaseModel):
    title: str
    excerpt: str | None = None
    content: str
    status: PostStatus
    category_id: UUID


class PostCreate(PostBase):
    tag_ids: list[UUID] = Field(default_factory=list)

    @classmethod
    def get_form(
        cls,
        title: str = Form(...),
        excerpt: str | None = Form(None),
        content: str = Form(...),
        status: PostStatus = Form(...),
        category_id: UUID = Form(...),
        tag_ids: list[UUID] = Form([]),
    ):
        return cls(
            title=title,
            excerpt=excerpt,
            content=content,
            status=status,
            category_id=category_id,
            tag_ids=tag_ids,
        )


class PostUpdate(BaseModel):
    title: str | None = None
    excerpt: str | None = None
    content: str | None = None
    status: PostStatus | None = None
    category_id: UUID | None = None
    tag_ids: list[UUID] | None = None

    @classmethod
    def get_form(
        cls,
        title: str | None = Form(None),
        excerpt: str | None = Form(None),
        content: str | None = Form(None),
        status: PostStatus | None = Form(None),
        category_id: UUID | None = Form(None),
        tag_ids: list[UUID] | None = Form(None),
    ):
        return cls(
            title=title,
            excerpt=excerpt,
            content=content,
            status=status,
            category_id=category_id,
            tag_ids=tag_ids,
        )


class PostAuthorResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    avatar: str | None = None

    @computed_field
    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    model_config = ConfigDict(from_attributes=True)


class PostCategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


class PostTagResponse(BaseModel):
    id: UUID
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


class PostImageResponse(BaseModel):
    id: UUID
    image_url: str
    alt_text: str
    position: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    excerpt: str | None
    content: str
    cover_image: str | None
    status: PostStatus

    author_id: UUID
    category_id: UUID
    author: PostAuthorResponse
    category: PostCategoryResponse
    tags: list[PostTagResponse] = Field(default_factory=list)
    images: list[PostImageResponse] = Field(default_factory=list)

    published_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
