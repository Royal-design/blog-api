from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_bookmark_service
from app.models.user import User
from app.schemas.bookmark import BookmarkedPostResponse, BookmarkResponse
from app.schemas.response import SuccessResponse
from app.services.bookmark_service import BookmarkService

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/me", response_model=SuccessResponse[list[BookmarkedPostResponse]])
def get_my_bookmarks(
    current_user: Annotated[User, Depends(get_current_user)],
    bookmark_service: Annotated[BookmarkService, Depends(get_bookmark_service)],
):
    bookmarks = bookmark_service.get_my_bookmarks(current_user.id)

    return SuccessResponse(
        message="Bookmarked posts retrieved successfully",
        data=bookmarks,
    )


@router.post(
    "/posts/{post_id}",
    response_model=SuccessResponse[BookmarkResponse],
    status_code=status.HTTP_201_CREATED,
)
def bookmark_post(
    post_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    bookmark_service: Annotated[BookmarkService, Depends(get_bookmark_service)],
):
    bookmark = bookmark_service.bookmark_post(current_user.id, post_id)

    return SuccessResponse(
        message="Post bookmarked successfully",
        data=bookmark,
    )


@router.delete("/posts/{post_id}", response_model=SuccessResponse[None])
def remove_bookmark(
    post_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    bookmark_service: Annotated[BookmarkService, Depends(get_bookmark_service)],
):
    bookmark_service.remove_bookmark(current_user.id, post_id)

    return SuccessResponse(
        message="Bookmark removed successfully",
        data=None,
    )
