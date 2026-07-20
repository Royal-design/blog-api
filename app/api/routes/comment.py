from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_comment_service
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from app.schemas.response import SuccessResponse
from app.services.comment_service import CommentService

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=SuccessResponse[list[CommentResponse]])
def get_comments(
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
    post_id: UUID | None = Query(default=None),
):
    comments = (
        comment_service.get_comments_by_post_id(post_id)
        if post_id
        else comment_service.get_all_comments()
    )

    return SuccessResponse(
        message="Comments retrieved successfully",
        data=comments,
    )


@router.get("/{comment_id}", response_model=SuccessResponse[CommentResponse])
def get_comment(
    comment_id: UUID,
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
):
    comment = comment_service.get_comment_by_id(comment_id)

    return SuccessResponse(
        message="Comment retrieved successfully",
        data=comment,
    )


@router.post(
    "/",
    response_model=SuccessResponse[CommentResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    request: CommentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
):
    comment = comment_service.create_comment(request, current_user)

    return SuccessResponse(
        message="Comment created successfully",
        data=comment,
    )


@router.put("/{comment_id}", response_model=SuccessResponse[CommentResponse])
def update_comment(
    comment_id: UUID,
    request: CommentUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
):
    comment = comment_service.update_comment(comment_id, request, current_user)

    return SuccessResponse(
        message="Comment updated successfully",
        data=comment,
    )


@router.delete("/{comment_id}", response_model=SuccessResponse[None])
def delete_comment(
    comment_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
):
    comment_service.delete_comment(comment_id, current_user)

    return SuccessResponse(
        message="Comment deleted successfully",
        data=None,
    )
