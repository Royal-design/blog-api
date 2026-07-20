from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_follow_service
from app.models.user import User
from app.schemas.follow import FollowerResponse, FollowingResponse, FollowResponse
from app.schemas.response import SuccessResponse
from app.services.follow_service import FollowService

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/followers/{user_id}", response_model=SuccessResponse[list[FollowerResponse]])
def get_followers(
    user_id: UUID,
    follow_service: Annotated[FollowService, Depends(get_follow_service)],
):
    followers = follow_service.get_followers(user_id)

    return SuccessResponse(
        message="Followers retrieved successfully",
        data=followers,
    )


@router.get("/following/{user_id}", response_model=SuccessResponse[list[FollowingResponse]])
def get_following(
    user_id: UUID,
    follow_service: Annotated[FollowService, Depends(get_follow_service)],
):
    following = follow_service.get_following(user_id)

    return SuccessResponse(
        message="Following retrieved successfully",
        data=following,
    )


@router.post(
    "/{user_id}",
    response_model=SuccessResponse[FollowResponse],
    status_code=status.HTTP_201_CREATED,
)
def follow_user(
    user_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    follow_service: Annotated[FollowService, Depends(get_follow_service)],
):
    follow = follow_service.follow_user(current_user.id, user_id)

    return SuccessResponse(
        message="User followed successfully",
        data=follow,
    )


@router.delete("/{user_id}", response_model=SuccessResponse[None])
def unfollow_user(
    user_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    follow_service: Annotated[FollowService, Depends(get_follow_service)],
):
    follow_service.unfollow_user(current_user.id, user_id)

    return SuccessResponse(
        message="User unfollowed successfully",
        data=None,
    )
