from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router
from app.api.routes.profile import router as profile_router
from app.api.routes.category import router as category_router
from app.api.routes.bookmark import router as bookmark_router
from app.api.routes.comment import router as comment_router
from app.api.routes.follow import router as follow_router
from app.api.routes.like import router as like_router
from app.api.routes.tag import router as tag_router
from app.api.routes.post import router as post_router





api_router = APIRouter()

def includes_api_routes(api: APIRouter):
    api.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
    api.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
    api.include_router(profile_router, prefix="/api/v1/profile", tags=["Profile"])
    api.include_router(category_router, prefix="/api/v1/categories", tags=["Categories"])
    api.include_router(tag_router, prefix="/api/v1/tags", tags=["Tags"])
    api.include_router(post_router, prefix="/api/v1/posts", tags=["Posts"])
    api.include_router(comment_router, prefix="/api/v1/comments", tags=["Comments"])
    api.include_router(like_router, prefix="/api/v1/likes", tags=["Likes"])
    api.include_router(bookmark_router, prefix="/api/v1/bookmarks", tags=["Bookmarks"])
    api.include_router(follow_router, prefix="/api/v1/follows", tags=["Follows"])
    
    
    
    

includes_api_routes(api_router)
