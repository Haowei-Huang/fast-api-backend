from typing import Annotated
from fastapi import APIRouter, Depends, Cookie, Response, Request
from dependencies.dependencies import get_user_service, get_current_user
from models.user import User
from schemas.user.request.login_request import LoginRequest
from schemas.user.response.login_response import LoginResponse
from schemas.user.response.refresh_token_response import RefreshTokenResponse
from schemas.user.response.user_create_response import UserCreateResponse
from schemas.user.response.user_delete_response import UserDeleteResponse
from schemas.user.response.user_get_response import UserGetResponse
from schemas.user.response.user_list_response import UserListResponse
from schemas.user.response.user_update_response import UserUpdateResponse
from schemas.user.request.user_request import UserRequest
from service.user_service import UserService
from exceptions.custom_exception import TokenNotFoundError
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO or DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format for log messages
)

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/register", response_model=UserCreateResponse)
async def create_user(
    req: UserRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(req)


@router.post("/login", response_model=LoginResponse)
async def login(
    req: LoginRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
    response: Response,
):
    return await user_service.login(req, response)


@router.post("/logout")
async def logout(
    user_service: Annotated[UserService, Depends(get_user_service)],
    response: Response,
    refreshToken: Annotated[str | None, Cookie(alias="refreshToken")] = None,
):
    if refreshToken is None:
        return {"message": "No refresh token provided."}
    return await user_service.logout(refreshToken, response)


@router.post("/refreshAccessToken", response_model=RefreshTokenResponse)
async def refresh_access_token(
    user_service: Annotated[UserService, Depends(get_user_service)],
    response: Response,
    refreshToken: Annotated[str | None, Cookie(alias="refreshToken")] = None,
):
    if refreshToken is None:
        logging.info(f"No refresh token provided")
        raise TokenNotFoundError("No refresh token provided")
    return await user_service.refresh_access_token(response, refreshToken)


@router.put(
    "/updateUser/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserUpdateResponse,
)
async def update_user(
    user_id: str,
    req: UserRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update(user_id, req)


@router.delete(
    "/deleteUser/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserDeleteResponse,
)
async def delete_user(
    user_id: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.delete(user_id)


@router.get(
    "/findAllUsers",
    dependencies=[Depends(get_current_user)],
    response_model=UserListResponse,
)
async def find_all_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.find_all()


@router.get("/findUserByEmail/{email}", response_model=UserGetResponse)
async def find_user_by_email(
    email: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.get_by_email(email)


@router.get(
    "/findUserById/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserGetResponse,
)
async def find_user_by_id(
    user_id: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.get_by_id(user_id)
