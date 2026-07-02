from fastapi import APIRouter

from app.api.routes.auth import router as authRouter


api_router = APIRouter()

def includes_api_routes(api: APIRouter):
    api.include_router(authRouter, prefix="/api/v1/auth", tags=["auth"])
    

includes_api_routes(api_router)
