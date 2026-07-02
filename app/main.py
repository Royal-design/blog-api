from fastapi import FastAPI
from app.api.router import includes_api_routes

app = FastAPI()

includes_api_routes(app)

