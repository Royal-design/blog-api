from app.schemas.category import CategoryCreate, CategoryUpdate
from slugify import slugify

from app.core.exceptions import AppException
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def get_all_categories(self):
        return self.category_repository.get_all_categories()

    def get_category_by_id(self, category_id: str):
        category = self.category_repository.get_category_by_id(category_id)

        if not category:
            raise AppException(
                message="Category not found",
                status_code=404,
            )

        return category

    def create_category(self, request: CategoryCreate):
        slug = slugify(request.name)

        existing = self.category_repository.get_category_by_slug(slug)

        if existing:
            raise AppException(
                message="Category already exists",
                status_code=400,
            )

        category = Category(
            name=request.name,
            slug=slug,
        )

        return self.category_repository.create_category(category)

    def update_category(self, category_id: str, request:CategoryUpdate):
        category = self.category_repository.get_category_by_id(category_id)

        if not category:
            raise AppException(
                message="Category not found",
                status_code=404,
            )

        slug = slugify(request.name)

        existing = self.category_repository.get_category_by_slug(slug)

        if existing and existing.id != category.id:
            raise AppException(
                message="Category already exists",
                status_code=400,
            )

        category.name = request.name
        category.slug = slug

        return self.category_repository.update_category(category)

    def delete_category(self, category_id: str):
        category = self.category_repository.get_category_by_id(category_id)

        if not category:
            raise AppException(
                message="Category not found",
                status_code=404,
            )

        self.category_repository.delete_category(category)