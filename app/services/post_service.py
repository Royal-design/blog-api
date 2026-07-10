from datetime import datetime, timezone
from uuid import UUID

from fastapi import UploadFile
from slugify import slugify

from app.core.exceptions import AppException
from app.models.enums import PostStatus
from app.models.post import Post
from app.models.post_image import PostImage
from app.models.user import User
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
    
    def _check_post_permission(
        self,
        post: Post,
        current_user: User,
    ):
        if (
            post.author_id != current_user.id
            # and current_user.role != UserRole.ADMIN
        ):
            raise AppException(
                status_code=403,
                detail="You are not authorized to perform this action.",
            )

    def _build_post_images(
        self,
        images: list[UploadFile] | None,
        alt_texts: list[str] | None,
        positions: list[int] | None,
        fallback_alt: str,
    ) -> list[PostImage]:
        if not images:
            return []

        post_images = []
        for index, image in enumerate(images):
            uploaded = self.cloudinary_service.upload_image(
                image,
                folder="posts",
            )
            
            alt_text = (
                alt_texts[index]
                if alt_texts and index < len(alt_texts) and alt_texts[index]
                else fallback_alt
            )
            position = (
                positions[index]
                if positions and index < len(positions)
                else index
            )

            post_images.append(
                PostImage(
                    image_url=uploaded["url"],
                    alt_text=alt_text,
                    position=position,
                )
            )

        return post_images

    def create_post(
        self,
        post: PostCreate,
        author_id: UUID,
        cover_image: UploadFile | None = None,
        images: list[UploadFile] | None = None,
        image_alt_texts: list[str] | None = None,
        image_positions: list[int] | None = None,
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

        db_post.images = self._build_post_images(
            images=images,
            alt_texts=image_alt_texts,
            positions=image_positions,
            fallback_alt=post.title,
        )

        return self.post_repository.create_post(db_post)

    def update_post(
        self,
        post_id: UUID,
        current_user: User,
        post: PostUpdate,
        cover_image: UploadFile | None = None,
        images: list[UploadFile] | None = None,
        image_alt_texts: list[str] | None = None,
        image_positions: list[int] | None = None,
        delete_image_ids: list[UUID] | None = None,
    ):
        db_post = self.get_post_by_id(post_id)

        self._check_post_permission(db_post, current_user)

        update_data = post.model_dump(
            exclude_unset=True,
            exclude={"tag_ids"},
        )

        if "category_id" in update_data:
            self.category_service.get_category_by_id(
                update_data["category_id"]
            )

        if (
            "title" in update_data
            and update_data["title"] != db_post.title
        ):
            update_data["slug"] = self._generate_unique_slug(
                update_data["title"]
            )

        if (
            update_data.get("status") == PostStatus.PUBLISHED
            and db_post.published_at is None
        ):
            update_data["published_at"] = datetime.now(timezone.utc)

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

        for key, value in update_data.items():
            setattr(db_post, key, value)

        if post.tag_ids is not None:
            db_post.tags = self.tag_service.get_tags_by_ids(post.tag_ids)

        if delete_image_ids:
            delete_image_id_set = set(delete_image_ids)
            existing_image_ids = {image.id for image in db_post.images}
            invalid_image_ids = delete_image_id_set - existing_image_ids

            if invalid_image_ids:
                raise AppException(
                    status_code=404,
                    detail="One or more post images were not found.",
                )

            db_post.images = [
                image
                for image in db_post.images
                if image.id not in delete_image_id_set
            ]

        new_images = self._build_post_images(
            images=images,
            alt_texts=image_alt_texts,
            positions=image_positions,
            fallback_alt=post.title or db_post.title,
        )
        if new_images:
            db_post.images.extend(new_images)

        return self.post_repository.update_post(db_post)
    
    def delete_post(
        self,
        post_id: UUID,
        current_user: User,
    ):
        post = self.get_post_by_id(post_id)

        self._check_post_permission(post, current_user)

        if post.cover_image_public_id:
            self.cloudinary_service.delete_image(
                post.cover_image_public_id
            )

        return self.post_repository.delete_post(post)
