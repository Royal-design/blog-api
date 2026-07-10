from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.router import includes_api_routes
from app.core.app_exception_handler import app_exception_handler
from app.core.exceptions import AppException
import app.models

app = FastAPI()

includes_api_routes(app)

app.add_exception_handler(AppException, app_exception_handler)


def _mark_upload_fields_as_binary(schema_part: Any) -> None:
    if isinstance(schema_part, dict):
        if schema_part.get("contentMediaType") == "application/octet-stream":
            schema_part["format"] = "binary"

        for value in schema_part.values():
            _mark_upload_fields_as_binary(value)

    if isinstance(schema_part, list):
        for item in schema_part:
            _mark_upload_fields_as_binary(item)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    _mark_upload_fields_as_binary(openapi_schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

