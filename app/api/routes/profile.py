from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_user_service
from app.models.user import User
from app.schemas.response import SuccessResponse
from app.schemas.user import UserProfileRequest, UserResponse
from app.services.user_service import UserService

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=SuccessResponse[UserResponse])
def update_profile(
    request: UserProfileRequest = Depends(UserProfileRequest.get_form),
    avatar: UploadFile | None = File(None),  
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    result = user_service.update_profile(
        user_id=current_user.id,
        request=request,
        avatar=avatar,
    )
    return SuccessResponse(
        message="Profile updated successfully",
        data=result
    )