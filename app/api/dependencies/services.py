from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.category_repository import CategoryRepository
from app.repositories.post_repository import PostRepository
from app.repositories.tag_repository import TagRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.cloudinary_service import CloudinaryService
from app.services.email_service import EmailService
from app.services.post_service import PostService
from app.services.tag_service import TagService
from app.services.user_service import UserService



def get_user_service(db:Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    cloudinaary_service = CloudinaryService()
    return UserService(repository, cloudinaary_service)

def get_email_service():
    return EmailService()


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
    email_service: EmailService = Depends(get_email_service),
):
    return AuthService(
        user_service=user_service,
        email_service=email_service,
    )

def get_cloudinary_service():
    return CloudinaryService()

def get_category_service(db:Session = Depends(get_db)):
    category_repository = CategoryRepository(db)
    return CategoryService(category_repository)

def get_tag_service(db:Session = Depends(get_db)):
    tag_repository = TagRepository(db)
    return TagService(tag_repository)


def get_post_service(db:Session = Depends(get_db)):
    post_repository = PostRepository(db)
    category_service = get_category_service(db)
    tag_service = get_tag_service(db)
    cloudinary_service = get_cloudinary_service()
    return PostService(post_repository, category_service, tag_service, cloudinary_service)