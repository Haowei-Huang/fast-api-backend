from typing import Annotated
from fastapi import APIRouter, Depends
from dependencies.dependencies import get_user_service
from models.user import User
from schemas.user.response.user_create_response import UserCreateResponse
from schemas.user.response.user_delete_response import UserDeleteResponse
from schemas.user.response.user_get_response import UserGetResponse
from schemas.user.response.user_list_response import UserListResponse
from schemas.user.response.user_update_response import UserUpdateResponse
from schemas.user.request.user_request import UserRequest
from service.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserCreateResponse)
async def create_user(
    req: UserRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(req)


@router.put("/updateUser/{user_id}", response_model=UserUpdateResponse)
async def update_user(
    user_id: str,
    req: UserRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update(user_id, req)


@router.delete("/deleteUser/{user_id}", response_model=UserDeleteResponse)
async def delete_user(
    user_id: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.delete(user_id)


@router.get("/findAllUsers", response_model=UserListResponse)
async def find_all_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.find_all()


@router.get("/findUserByEmail/{email}", response_model=UserGetResponse)
async def find_user_by_email(
    email: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.get_by_email(email)


@router.get("/findUserById/{user_id}", response_model=UserGetResponse)
async def find_user_by_id(
    user_id: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.get_by_id(user_id)
