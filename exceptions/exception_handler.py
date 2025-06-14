from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from exceptions.custom_exception import (
    AuthenticationError,
    NotFoundError,
    UserAlreadyExistsError,
)
from jwt import InvalidTokenError


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": f"An unexpected error occurred, error: {str(exc)}"},
        )

    @app.exception_handler(InvalidTokenError)
    async def expired_token_handler(request: Request, exc: InvalidTokenError):
        return JSONResponse(
            status_code=401,
            content={"message": str(exc)},
        )

    @app.exception_handler(AuthenticationError)
    async def token_not_found_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=401,
            content={"message": str(exc)},
        )

    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_handler(
        request: Request, exc: UserAlreadyExistsError
    ):
        return JSONResponse(
            status_code=409,
            content={"message": str(exc)},
        )

    @app.exception_handler(NotFoundError)
    async def user_not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"message": str(exc)},
        )
