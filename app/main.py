from fastapi import FastAPI
from app.api.router import includes_api_routes
from app.core.app_exception_handler import app_exception_handler
from app.core.exceptions import AppException
import app.models

app = FastAPI()

includes_api_routes(app)

app.add_exception_handler(AppException, app_exception_handler)

