from hmac import new
from os import name
from re import S

from slugify import slugify
from app.core.exceptions import AppException
from app.models import tag
from app.models.tag import Tag
from app.repositories.tag_repository import TagRepository
from app.schemas.tag import TagRequest


class TagService:
    def __init__(self, tag_repository:TagRepository):
        self.tag_repository = tag_repository
        
    def get_all_tags(self):
        return self.tag_repository.get_all_tags()
    
    def get_tag_by_id(self, tag_id: str):
        return self.tag_repository.get_tag_by_id(tag_id)
    
    def get_tag_by_slug(self, slug: str):
        return self.tag_repository.get_tag_by_slug(slug)
    
    def create_tag(self, tag:TagRequest):
        slug  = slugify(tag.name)
        existing = self.tag_repository.get_tag_by_slug(slug)
        if existing:
            raise AppException(
                message="Tag already exists",
                status_code=400,
            )
        
        new_tag = Tag(
            name=tag.name,
            slug=slug,
        )
        return self.tag_repository.create_tag(new_tag)

    def update_tag(self, tag_id: str, request: TagRequest):
        tag = self.tag_repository.get_tag_by_id(tag_id)
        if not tag:
            raise AppException(
                message="Tag not found",
                status_code=404,
            )
        
        slug = slugify(request.name)
        existing = self.tag_repository.get_tag_by_slug(slug)
        if existing and existing.id != tag.id:
            raise AppException(
                message="Tag already exists",
                status_code=400,
            )
        tag.name = request.name
        tag.slug = slug
        return self.tag_repository.update_tag(tag)
    
    def delete_tag(self, tag_id: str):
        tag = self.tag_repository.get_tag_by_id(tag_id)
        if not tag:
            raise AppException(
                message="Tag not found",
                status_code=404,
            )
        return self.tag_repository.delete_tag(tag)