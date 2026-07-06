from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_user_service
from app.schemas.response import SuccessResponse
from app.schemas.user import UserResponse, UserUpdateRequest
from app.services.user_service import UserService

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/users", response_model=SuccessResponse[list[UserResponse]])
def get_users(
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    user_service: UserService = Depends(get_user_service),
):
    result = user_service.get_all_users(
        search=search,
        page=page,
        page_size=page_size,
    )

    return SuccessResponse(
        message="Users retrieved successfully",
        data=result["data"],
        meta=result["meta"]
    )

@router.put("/users/{user_id}", response_model=SuccessResponse[UserResponse])
def update_user(user_id: UUID, user: UserUpdateRequest, user_service: UserService = Depends(get_user_service)):
    user = user_service.update_user(user_id, user)
    return SuccessResponse(
        message="User updated successfully",
        data=user
        
    )

@router.delete("/users/{user_id}", response_model=SuccessResponse[UserResponse])
def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    user = user_service.delete_user(user_id)
    return SuccessResponse(
        message="User deleted successfully",
        data=user
    )
    