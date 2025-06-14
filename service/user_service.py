import datetime
from fastapi.params import Cookie
from typing_extensions import Annotated
from bson import ObjectId
from exceptions.user_identifier import UserIdentifier
from models.refresh_token_in_db import RefreshTokenInDB
from repository.user_repository import IUserRepository
from repository.refresh_token_repository import IRefreshTokenRepository
from models.user import User
import inspect
import logging
from schemas.user.request.login_request import LoginRequest
from schemas.user.response.login_response import LoginResponse
from schemas.user.response.user_create_response import UserCreateResponse
from schemas.user.response.user_delete_response import UserDeleteResponse
from schemas.user.response.user_list_response import UserListResponse
from schemas.user.response.user_get_response import UserGetResponse
from schemas.user.response.user_update_response import UserUpdateResponse
from schemas.user.request.user_request import UserRequest
from schemas.user.response.refresh_token_response import RefreshTokenResponse
from exceptions.custom_exception import (
    AuthenticationError,
    TokenNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserServiceError,
    WrongCredentialsError,
)
from util.auth import AuthUtils
from config.auth.auth_settings import AuthSettings
from fastapi import Response

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO or DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format for log messages
)


class UserService:
    def __init__(
        self,
        auth_settings: AuthSettings,
        user_repository: IUserRepository,
        refresh_token_repository: IRefreshTokenRepository,
    ):
        self.auth_settings = auth_settings
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    async def find_all(self) -> UserListResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            users = await self.user_repository.find_all()
            return UserListResponse(data=users, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise UserServiceError(f"Failed to retrieve users: {str(e)}")
            # return UserListResponse(data=[], error=str(e))

    async def get_by_id(self, user_id: str) -> UserGetResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            user = await self.user_repository.get_by_id(user_id)
            return UserGetResponse(data=user, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise UserServiceError(f"Failed to find user with id {user_id}: {str(e)}")
            # return UserGetResponse(data=None, error=str(e))

    async def get_by_email(self, email: str) -> UserGetResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called: {email}")
            user = await self.user_repository.get_by_email(email.lower())
            return UserGetResponse(data=user, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise UserServiceError(f"Failed to find user with email {email}: {str(e)}")
            # return UserGetResponse(data=None, error=str(e))

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

            req.password = AuthUtils.get_hashed_password(req.password)
            user = User(**req.model_dump(by_alias=True, exclude_unset=True))
            inserted_id = await self.user_repository.create_user(user)

            if not inserted_id:
                raise UserServiceError()

            # verify creation
            created_user = await self.user_repository.get_by_id(inserted_id)
            if not created_user:
                raise UserServiceError()

            return UserCreateResponse(is_created=True, data=inserted_id, error=None)
        except UserAlreadyExistsError as e:
            logging.error(f"User already exists: {str(e)}")
            raise e
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise UserServiceError(f"Failed to create user: {str(e)}")
            # return UserCreateResponse(is_created=False, data=None, error=str(e))

    async def delete(self, user_id: str) -> UserDeleteResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            await self.user_repository.delete(user_id)

            user = await self.user_repository.get_by_id(user_id)
            if user:
                raise UserServiceError()

            return UserDeleteResponse(is_deleted=True, user_id=user_id, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise UserServiceError(f"Failed to delete user with id {user_id}: {str(e)}")
            # return UserDeleteResponse(is_deleted=False, user_id=None, error=str(e))

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
                raise UserServiceError()

            updated_user = await self.user_repository.get_by_id(user_id)
            return UserUpdateResponse(is_updated=True, data=updated_user, error=None)
        except UserAlreadyExistsError as e:
            logging.error(f"User already exists: {str(e)}")
            raise e
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise UserServiceError(f"Failed to update user with id {user_id}: {str(e)}")
            # return UserUpdateResponse(is_updated=False, data=None, error=str(e))

    async def login(self, req: LoginRequest, response: Response) -> LoginResponse:
        try:
            email = req.email.lower()
            password = req.password
            logging.info(f"{inspect.stack()[1][3]} called")
            user = await self.user_repository.get_by_email(email.lower())
            if not user or not user.id:
                raise UserNotFoundError(UserIdentifier.email, email)

            hashed_password = AuthUtils.get_hashed_password(password)
            if not (
                password == user.password
                or AuthUtils.verify_password(password, hashed_password)
            ):
                raise WrongCredentialsError("Incorrect password")

            to_encode = {
                "email": str(email),
                "iss": "fast api backend",
                "aud": "simplii-book",
            }

            access_token: str = AuthUtils.generate_access_token(
                data=to_encode,
                secret_key=self.auth_settings.access_token_private_key,
                algorithm=self.auth_settings.algorithm,
            )

            refresh_token: dict = AuthUtils.generate_refresh_token(
                data=to_encode,
                secret_key=self.auth_settings.refresh_token_private_key,
                algorithm=self.auth_settings.algorithm,
            )

            token_in_db = RefreshTokenInDB(
                userId=user.id,
                token=refresh_token["token"],
                createdAt=datetime.datetime.now(datetime.timezone.utc),
                expiredAt=refresh_token["exp"],
            )
            # store refresh token in the database
            inserted_id = await self.refresh_token_repository.create_refresh_token(
                tokenInDB=token_in_db
            )

            if not inserted_id:
                raise UserServiceError(
                    f"Failed to create refresh token for user {user.id}"
                )

            # created_token = await self.refresh_token_repository.get_by_id(inserted_id)

            # if not created_token:
            #     raise RefreshTokenCreationError(
            #         f"Failed to create refresh token for user {user.id}"
            #     )
            # set refresh token in the response cookie
            response.set_cookie(
                key="refreshToken",
                value=refresh_token["token"],
                httponly=True,
                max_age=1 * 60 * 60,  # 1 hour
                secure=False,  # For development
            )

            return LoginResponse(
                message="Login successful",
                user=user,
                token=access_token,
            )
        except WrongCredentialsError as e:
            logging.error(f"Wrong credentials: {str(e)}")
            raise e
        except UserNotFoundError as e:
            logging.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise UserServiceError(
                f"Failed to login user with email {req.email}: {str(e)}"
            )
            # return LoginResponse(
            #     message="Something went wrong when trying to login", error=str(e)
            # )

    async def refresh_access_token(
        self, response: Response, refreshToken: str
    ) -> RefreshTokenResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")

            refreshTokenInDB = await self.refresh_token_repository.get_by_token(
                refreshToken
            )
            if not refreshTokenInDB:
                logging.info(f"Refresh token {refreshToken} not found in the database")
                raise TokenNotFoundError(f"Refresh token {refreshToken} not found")

            # raise error if invalid
            res = AuthUtils.verify_token(
                refreshToken, self.auth_settings.refresh_token_public_key
            )

            logging.info(f"Refresh token is valid")

            # generate new access token and refresh token
            to_encode = {
                "email": str(res["email"]),
                "iss": "fast api backend",
                "aud": "simplii-book",
            }

            new_access_token: str = AuthUtils.generate_access_token(
                data=to_encode,
                secret_key=self.auth_settings.access_token_private_key,
                algorithm=self.auth_settings.algorithm,
            )

            new_refresh_token: dict = AuthUtils.generate_refresh_token(
                data=to_encode,
                secret_key=self.auth_settings.refresh_token_private_key,
                algorithm=self.auth_settings.algorithm,
            )

            # update refresh token in the database
            modified_count = await self.refresh_token_repository.update(
                token=refreshToken, newToken=new_refresh_token["token"]
            )

            if modified_count != 1:
                raise UserServiceError(
                    f"Failed to update refresh Token with email {res['email']}"
                )

            response.set_cookie(
                key="refreshToken",
                value=new_refresh_token["token"],
                httponly=True,
                max_age=1 * 60 * 60,  # 1 hour
                secure=False,  # For development
            )

            return RefreshTokenResponse(
                message="Access token refreshed successfully", token=new_access_token
            )
        except TokenNotFoundError as e:
            raise e
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise UserServiceError(f"Failed to refresh access token: {str(e)}")
            # return RefreshTokenResponse(
            #     message="Something went wrong when trying to refresh access token",
            #     error=str(e),
            # )

    async def logout(self, token: str, response: Response):
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            await self.refresh_token_repository.delete(token)

            is_present = await self.refresh_token_repository.get_by_token(token)
            if is_present:
                raise UserServiceError(f"Failed to delete refresh token {token}")

            response.delete_cookie(key="refreshToken", httponly=True)
            return {"message": "Logout successful"}
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise UserServiceError(
                f"Failed to logout user with token {token}: {str(e)}"
            )
            # return {
            #     "message": "Something went wrong when trying to logout",
            #     "error": str(e),
            # }
