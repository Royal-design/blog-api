from fastapi import APIRouter, Depends, status
from uuid import UUID

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_category_service
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.response import SuccessResponse
from app.services.category_service import CategoryService

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", response_model=SuccessResponse[list[CategoryResponse]])
def get_categories(category_service: CategoryService = Depends(get_category_service)):
    categories = category_service.get_all_categories()

    return SuccessResponse(
        message="Categories retrieved successfully",
        data=categories,
    )

@router.post("/", response_model=SuccessResponse[CategoryResponse],status_code=status.HTTP_201_CREATED)
def create_category(
    request: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
    
):
    category = category_service.create_category(request)

    return SuccessResponse(
        message="Category created successfully",
        data=category,
    )

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: UUID, category_service: CategoryService = Depends(get_category_service)):
    category = category_service.get_category_by_id(category_id)

    return category

@router.get("/slug/{slug}", response_model=CategoryResponse)
def get_category(slug_name: str, category_service: CategoryService = Depends(get_category_service)):
    category = category_service.get_category_by_slug(slug_name)
    return category


@router.put("/{category_id}", response_model=SuccessResponse[CategoryResponse])
def update_category(
    category_id: UUID,
    request: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
):
    category = category_service.update_category(category_id, request)

    return SuccessResponse(
        message="Category updated successfully",
        data=category,
    )

@router.delete("/{category_id}", response_model=SuccessResponse[CategoryResponse])
def delete_category(
    category_id: UUID,
    category_service: CategoryService = Depends(get_category_service),
):
    category = category_service.delete_category(category_id)

    return SuccessResponse(
        message="Category deleted successfully",
        data=category,
    )

