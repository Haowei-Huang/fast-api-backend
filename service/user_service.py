from bson import ObjectId
from repository.user_repository import IUserRepository
from models.user import User
import inspect
import logging
from fastapi.encoders import jsonable_encoder
from schemas.user.response.user_create_response import UserCreateResponse
from schemas.user.response.user_delete_response import UserDeleteResponse
from schemas.user.response.user_list_response import UserListResponse
from schemas.user.response.user_get_response import UserGetResponse
from schemas.user.response.user_update_response import UserUpdateResponse
from schemas.user.request.user_request import UserRequest
from exceptions.custom_exception import (
    UserCreationError,
    UserAlreadyExistsError,
    UserDeletionError,
    UserUpdateError,
)
from passlib.context import CryptContext


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def find_all(self) -> UserListResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            users = await self.user_repository.find_all()
            return UserListResponse(data=users, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return UserListResponse(data=[], error=str(e))

    async def get_by_id(self, user_id: str) -> UserGetResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            user = await self.user_repository.get_by_id(user_id)
            return UserGetResponse(data=user, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return UserGetResponse(data=None, error=str(e))

    async def get_by_email(self, email: str) -> UserGetResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            user = await self.user_repository.get_by_email(email.lower())
            return UserGetResponse(data=user, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return UserGetResponse(data=None, error=str(e))

    async def create_user(self, req: UserRequest) -> UserCreateResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            existing_user = await self.user_repository.get_by_email(
                str(req.email).lower()
            )
            if existing_user:
                raise UserAlreadyExistsError(
                    f"User with email {req.email} already exists"
                )

            req.password = self.__get_hashed_password(req.password)
            user = User(**req.model_dump(by_alias=True, exclude_unset=True))
            inserted_id = await self.user_repository.create_user(user)

            if not inserted_id:
                raise UserCreationError("Failed to create user")

            # verify creation
            created_user = await self.user_repository.get_by_id(inserted_id)
            if not created_user:
                raise UserCreationError("Failed to create user")

            return UserCreateResponse(is_created=True, data=inserted_id, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return UserCreateResponse(is_created=False, data=None, error=str(e))

    async def delete(self, user_id: str) -> UserDeleteResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            await self.user_repository.delete(user_id)

            user = await self.user_repository.get_by_id(user_id)
            if user:
                raise UserDeletionError(f"Failed to delete user with id {user_id}")

            return UserDeleteResponse(is_deleted=True, user_id=user_id, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return UserDeleteResponse(is_deleted=False, user_id=None, error=str(e))

    async def update(self, user_id: str, req: UserRequest) -> UserUpdateResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            # check if another user with the same email exists
            existing_user = await self.user_repository.get_by_email(
                str(req.email).lower()
            )
            if existing_user and str(existing_user.id) != user_id:
                raise UserAlreadyExistsError(
                    f"User with email {req.email} already exists"
                )

            user = User(**req.model_dump(by_alias=True, exclude_unset=True))

            modified_count = await self.user_repository.update(user_id, user)
            if modified_count != 1:
                raise UserUpdateError(f"Failed to update user with id {user_id}")

            updated_user = await self.user_repository.get_by_id(user_id)
            return UserUpdateResponse(is_updated=True, data=updated_user, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return UserUpdateResponse(is_updated=False, data=None, error=str(e))

    def __get_hashed_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
