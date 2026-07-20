from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.bookmark_repository import BookmarkRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.follow_repository import FollowRepository
from app.repositories.like_repository import LikeRepository
from app.repositories.post_repository import PostRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.tag_repository import TagRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.bookmark_service import BookmarkService
from app.services.category_service import CategoryService
from app.services.cloudinary_service import CloudinaryService
from app.services.comment_service import CommentService
from app.services.email_service import EmailService
from app.services.follow_service import FollowService
from app.services.like_service import LikeService
from app.services.post_service import PostService
from app.services.refresh_token_service import RefreshTokenService
from app.services.tag_service import TagService
from app.services.user_service import UserService



def get_user_service(db:Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    cloudinaary_service = CloudinaryService()
    return UserService(repository, cloudinaary_service)

def get_email_service():
    return EmailService()


def get_auth_service(
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
    email_service: EmailService = Depends(get_email_service),
):
    refresh_token_repository = RefreshTokenRepository(db)
    refresh_token_service = RefreshTokenService(refresh_token_repository)
    return AuthService(
        user_service=user_service,
        email_service=email_service,
        refresh_token_service=refresh_token_service,
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


def get_comment_service(db: Session = Depends(get_db)):
    comment_repository = CommentRepository(db)
    post_service = get_post_service(db)
    return CommentService(comment_repository, post_service)


def get_like_service(db: Session = Depends(get_db)):
    like_repository = LikeRepository(db)
    post_service = get_post_service(db)
    return LikeService(like_repository, post_service)


def get_bookmark_service(db: Session = Depends(get_db)):
    bookmark_repository = BookmarkRepository(db)
    post_service = get_post_service(db)
    return BookmarkService(bookmark_repository, post_service)


def get_follow_service(db: Session = Depends(get_db)):
    follow_repository = FollowRepository(db)
    user_service = get_user_service(db)
    return FollowService(follow_repository, user_service)
