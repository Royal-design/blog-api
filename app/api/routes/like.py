from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_like_service
from app.models.user import User
from app.schemas.like import LikedPostResponse, LikeResponse
from app.schemas.response import SuccessResponse
from app.services.like_service import LikeService

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/me", response_model=SuccessResponse[list[LikedPostResponse]])
def get_my_likes(
    current_user: Annotated[User, Depends(get_current_user)],
    like_service: Annotated[LikeService, Depends(get_like_service)],
):
    likes = like_service.get_my_likes(current_user.id)

    return SuccessResponse(
        message="Liked posts retrieved successfully",
        data=likes,
    )


@router.post(
    "/posts/{post_id}",
    response_model=SuccessResponse[LikeResponse],
    status_code=status.HTTP_201_CREATED,
)
def like_post(
    post_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    like_service: Annotated[LikeService, Depends(get_like_service)],
):
    like = like_service.like_post(current_user.id, post_id)

    return SuccessResponse(
        message="Post liked successfully",
        data=like,
    )


@router.delete("/posts/{post_id}", response_model=SuccessResponse[None])
def unlike_post(
    post_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    like_service: Annotated[LikeService, Depends(get_like_service)],
):
    like_service.unlike_post(current_user.id, post_id)

    return SuccessResponse(
        message="Post unliked successfully",
        data=None,
    )
