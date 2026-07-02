from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.router import includes_api_routes
from app.core.exceptions import EmailAlreadyExistsError, InvalidCredentialsError, InvalidTokenException, UserNotFoundError

app = FastAPI()

includes_api_routes(app)

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


@app.exception_handler(EmailAlreadyExistsError)
async def email_already_exists_handler(
    request: Request,
    exc: EmailAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
):
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message},
    )


@app.exception_handler(InvalidTokenException)
async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenException,
):
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message},
    )

