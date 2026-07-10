from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    status,
)

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_post_service
from app.models.user import User
from app.schemas.post import (
    PostCreate,
    PostResponse,
    PostUpdate,
)
from app.schemas.response import SuccessResponse
from app.services.post_service import PostService

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get(
    "/",
    response_model=SuccessResponse[list[PostResponse]],
)
def get_all_posts(
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    posts = post_service.get_all_posts()

    return SuccessResponse(
        message="Posts retrieved successfully.",
        data=posts,
    )


@router.get(
    "/{post_id}",
    response_model=SuccessResponse[PostResponse],
)
def get_post_by_id(
    post_id: UUID,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    post = post_service.get_post_by_id(post_id)

    return SuccessResponse(
        message="Post retrieved successfully.",
        data=post,
    )


@router.get(
    "/slug/{slug}",
    response_model=SuccessResponse[PostResponse],
)
def get_post_by_slug(
    slug: str,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    post = post_service.get_post_by_slug(slug)

    return SuccessResponse(
        message="Post retrieved successfully.",
        data=post,
    )


@router.post(
    "/",
    response_model=SuccessResponse[PostResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    post: Annotated[PostCreate, Depends(PostCreate.get_form)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_service: Annotated[PostService, Depends(get_post_service)],
    cover_image: UploadFile | None = File(None),
    images: list[UploadFile] | None = File(None),
    image_alt_texts: list[str] = Form([]),
    image_positions: list[int] = Form([]),
):
    created_post = post_service.create_post(
        post=post,
        author_id=current_user.id,
        cover_image=cover_image,
        images=images,
        image_alt_texts=image_alt_texts,
        image_positions=image_positions,
    )

    return SuccessResponse(
        message="Post created successfully.",
        data=created_post,
    )


@router.put(
    "/{post_id}",
    response_model=SuccessResponse[PostResponse],
)
def update_post(
    post_id: UUID,
    post: Annotated[PostUpdate, Depends(PostUpdate.get_form)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_service: Annotated[PostService, Depends(get_post_service)],
    cover_image: UploadFile | None = File(None),
    images: list[UploadFile] | None = File(None),
    image_alt_texts: list[str] = Form([]),
    image_positions: list[int] = Form([]),
    delete_image_ids: list[UUID] = Form([]),
):
    updated_post = post_service.update_post(
        post_id=post_id,
        current_user=current_user,
        post=post,
        cover_image=cover_image,
        images=images,
        image_alt_texts=image_alt_texts,
        image_positions=image_positions,
        delete_image_ids=delete_image_ids,
    )

    return SuccessResponse(
        message="Post updated successfully.",
        data=updated_post,
    )

@router.delete(
    "/{post_id}",
    response_model=SuccessResponse[None],
)
def delete_post(
    post_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    post_service.delete_post(
        post_id=post_id,
        current_user=current_user,
    )

    return SuccessResponse(
        message="Post deleted successfully.",
        data=None,
    )
