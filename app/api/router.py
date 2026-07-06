from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router
from app.api.routes.profile import router as profile_router
from app.api.routes.category import router as category_router
from app.api.routes.tag import router as tag_router




api_router = APIRouter()

def includes_api_routes(api: APIRouter):
    api.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
    api.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
    api.include_router(profile_router, prefix="/api/v1/profile", tags=["Profile"])
    api.include_router(category_router, prefix="/api/v1/categories", tags=["Categories"])
    api.include_router(tag_router, prefix="/api/v1/tags", tags=["Tags"])
    
    
    
    

includes_api_routes(api_router)
