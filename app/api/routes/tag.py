from fastapi import APIRouter, Depends, status
from uuid import UUID

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import  get_tag_service
from app.schemas.response import SuccessResponse
from app.schemas.tag import TagRequest, TagResponse
from app.services.tag_service import TagService

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", response_model=SuccessResponse[list[TagResponse]])
def get_tags(tag_service:TagService=Depends(get_tag_service)):
    tags = tag_service.get_all_tags()
    return SuccessResponse(
        message="Tags retrieved successfully",
        data=tags,
    )

@router.post("/", response_model=SuccessResponse[TagResponse], status_code=status.HTTP_201_CREATED)
def create_tag(
    request: TagRequest,
    tag_service: TagService = Depends(get_tag_service),
):
    tag = tag_service.create_tag(request)
    return SuccessResponse(
        message="Tag created successfully",
        data=tag,
    )

@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: UUID, tag_service: TagService = Depends(get_tag_service)):
    tag = tag_service.get_tag_by_id(tag_id)
    return tag

@router.put("/{tag_id}", response_model=SuccessResponse[TagResponse])
def update_tag(
    tag_id: UUID,
    request: TagRequest,
    tag_service: TagService = Depends(get_tag_service),
):
    tag = tag_service.update_tag(tag_id, request)
    return SuccessResponse(
        message="Tag updated successfully",
        data=tag,
    )

@router.delete("/{tag_id}", response_model=SuccessResponse[TagResponse])
def delete_tag(
    tag_id: UUID,
    tag_service: TagService = Depends(get_tag_service),
):
    tag = tag_service.delete_tag(tag_id)
    return SuccessResponse(
        message="Tag deleted successfully",
        data=tag,
    )   