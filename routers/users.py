from typing import Annotated
from fastapi import APIRouter, Depends
from dependencies.dependencies import get_user_service
from models.user import User
from schemas.user.create_user_response import CreateUserResponse
from schemas.user.delete_user_response import DeleteUserResponse
from schemas.user.get_user_response import GetUserResponse
from schemas.user.update_user_response import UpdateUserResponse
from service.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=CreateUserResponse)
async def create_user(
    user: User, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.create_user(user)


@router.put("/updateUser/{user_id}", response_model=UpdateUserResponse)
async def update_user(
    user_id: str,
    user: User,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update(user_id, user)


@router.delete("/deleteUser/{user_id}", response_model=DeleteUserResponse)
async def delete_user(
    user_id: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.delete(user_id)


@router.get("/findAllUsers", response_model=GetUserResponse)
async def find_all_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.find_all()


@router.get("/findUserByEmail/{email}", response_model=GetUserResponse)
async def find_user_by_email(
    email: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.get_by_email(email)


@router.get("/findUserById/{user_id}", response_model=GetUserResponse)
async def find_user_by_id(
    user_id: str, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.get_by_id(user_id)
