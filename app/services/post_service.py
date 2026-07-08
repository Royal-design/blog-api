from datetime import datetime, timezone
from uuid import UUID

from fastapi import UploadFile
from slugify import slugify

from app.core.exceptions import AppException
from app.models.enums import PostStatus
from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostUpdate
from app.services.category_service import CategoryService
from app.services.cloudinary_service import CloudinaryService
from app.services.tag_service import TagService


class PostService:
    def __init__(
        self,
        post_repository: PostRepository,
        category_service: CategoryService,
        tag_service: TagService,
        cloudinary_service: CloudinaryService,
    ):
        self.post_repository = post_repository
        self.category_service = category_service
        self.tag_service = tag_service
        self.cloudinary_service = cloudinary_service

    def get_all_posts(self):
        return self.post_repository.get_all_posts()

    def get_post_by_id(self, post_id: UUID):
        post = self.post_repository.get_post_by_id(post_id)

        if not post:
            raise AppException(
                status_code=404,
                detail="Post not found.",
            )

        return post

    def get_post_by_slug(self, slug: str):
        post = self.post_repository.get_post_by_slug(slug)

        if not post:
            raise AppException(
                status_code=404,
                detail="Post not found.",
            )

        return post

    def _generate_unique_slug(self, title: str) -> str:
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        while self.post_repository.get_post_by_slug(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def create_post(
        self,
        post: PostCreate,
        author_id: UUID,
        cover_image: UploadFile | None = None,
    ):
        # Validate category
        self.category_service.get_category_by_id(post.category_id)

        image_url = None
        public_id = None

        if cover_image:
            uploaded = self.cloudinary_service.upload_image(
                cover_image,
                folder="posts",
            )

            image_url = uploaded["url"]
            public_id = uploaded["public_id"]
            
        post_data = post.model_dump(exclude={"tag_ids"})

        db_post = Post(
            **post_data,
            slug=self._generate_unique_slug(post.title),
            author_id=author_id,
            cover_image=image_url,
            cover_image_public_id=public_id,
        )

       
        if post.status == PostStatus.PUBLISHED:
            db_post.published_at = datetime.now(timezone.utc)

        if post.tag_ids:
            db_post.tags = self.tag_service.get_tags_by_ids(post.tag_ids)

        return self.post_repository.create_post(db_post)

    def update_post(
        self,
        post_id: UUID,
        post: PostUpdate,
        cover_image: UploadFile | None = None,
    ):
        db_post = self.get_post_by_id(post_id)

        update_data = post.model_dump(
            exclude_unset=True,
            exclude={"tag_ids"},
        )

        # Validate category
        if "category_id" in update_data:
            self.category_service.get_category_by_id(
                update_data["category_id"]
            )

        # Generate a new slug if title changes
        if (
            "title" in update_data
            and update_data["title"] != db_post.title
        ):
            update_data["slug"] = self._generate_unique_slug(
                update_data["title"]
            )

        # Set published_at when publishing for the first time
        if (
            update_data.get("status") == PostStatus.PUBLISHED
            and db_post.published_at is None
        ):
            update_data["published_at"] = datetime.now(timezone.utc)

        # Upload new cover image
        if cover_image:
            if db_post.cover_image_public_id:
                self.cloudinary_service.delete_image(
                    db_post.cover_image_public_id
                )

            uploaded = self.cloudinary_service.upload_image(
                cover_image,
                folder="posts",
            )

            update_data["cover_image"] = uploaded["url"]
            update_data["cover_image_public_id"] = uploaded["public_id"]

        # Update all normal fields
        for key, value in update_data.items():
            setattr(db_post, key, value)

        # Update tags
        if post.tag_ids is not None:
            db_post.tags = self.tag_service.get_tags_by_ids(post.tag_ids)

        return self.post_repository.update_post(db_post)
    
    def delete_post(self, post_id: UUID):
        post = self.get_post_by_id(post_id)

        if post.cover_image_public_id:
            self.cloudinary_service.delete_image(
                post.cover_image_public_id
            )

        return self.post_repository.delete_post(post)