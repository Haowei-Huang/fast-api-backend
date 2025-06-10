from bson import ObjectId
from repository.user_repository import IUserRepository
from models.user import User
import inspect
import logging
from schemas.user.create_user_response import CreateUserResponse
from schemas.user.delete_user_response import DeleteUserResponse
from exceptions.custom_exception import (
    UserCreationError,
    UserAlreadyExistsError,
    UserDeletionError,
    UserUpdateError,
)
from schemas.user.get_user_response import GetUserResponse
from schemas.user.update_user_response import UpdateUserResponse
from passlib.context import CryptContext


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_by_id(self, user_id: str) -> GetUserResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            user = await self.user_repository.get_by_id(user_id)
            return GetUserResponse(data=user, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return GetUserResponse(data=None, error=str(e))

    async def get_by_email(self, email: str) -> GetUserResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            user = await self.user_repository.get_by_id(email.lower())
            return GetUserResponse(data=user, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return GetUserResponse(data=None, error=str(e))

    async def create_user(self, user: User) -> CreateUserResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            existing_user = await self.user_repository.get_by_email(
                str(user.email).lower()
            )
            if existing_user:
                raise UserAlreadyExistsError(
                    f"User with email {user.email} already exists"
                )

            user.password = self.__get_hashed_password(user.password)
            inserted_id = await self.user_repository.create_user(user)

            inserted_id = str(inserted_id)

            # verify creation
            created_user = await self.user_repository.get_by_id(inserted_id)
            if not created_user:
                raise UserCreationError("Failed to create user")

            return CreateUserResponse(is_created=True, data=inserted_id, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return CreateUserResponse(is_created=False, data=None, error=str(e))

    async def find_all(self) -> GetUserResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            users = await self.user_repository.find_all()
            return GetUserResponse(data=users, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return GetUserResponse(data=None, error=str(e))

    async def delete(self, user_id: str) -> DeleteUserResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            await self.user_repository.delete(user_id)

            user = await self.user_repository.get_by_id(user_id)
            if user:
                raise UserDeletionError(f"Failed to delete user with id {user_id}")

            return DeleteUserResponse(is_deleted=True, user_id=user_id, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return DeleteUserResponse(is_deleted=False, user_id=None, error=str(e))

    async def update(self, user_id: str, user_data: User) -> UpdateUserResponse:
        try:
            modified_count = await self.user_repository.update(user_id, user_data)
            if modified_count != 1:
                raise UserUpdateError(f"Failed to update user with id {user_id}")

            updated_user = await self.user_repository.get_by_id(user_id)
            return UpdateUserResponse(is_updated=True, data=updated_user, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return UpdateUserResponse(is_updated=False, data=None, error=str(e))

    def __get_hashed_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
