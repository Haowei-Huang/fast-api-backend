import logging

import jwt
from config.database_manager import DatabaseManager
from config.settings import Settings
from typing import Annotated
from fastapi import Depends, Header, Request
from config.database_manager import DatabaseType
from exceptions.custom_exception import TokenNotFoundError
from repository.booking_repository import IBookingRepository
from repository.hotel_repository import IHotelRepository
from repository.user_repository import IUserRepository
from service.booking_service import BookingService
from service.hotel_service import HotelService
from service.user_service import UserService
from config.auth.auth_settings import AuthSettings
from repository.refresh_token_repository import IRefreshTokenRepository
from util.auth import AuthUtils


def get_settings() -> Settings:
    return Settings()


def get_auth_settings():
    return AuthSettings()


def get_db_manager(request: Request) -> DatabaseManager:
    return request.app.state.db_manager


def get_current_user(
    auth_settings: Annotated[AuthSettings, Depends(get_auth_settings)],
    authorization: str = Header(None, alias="Authorization"),
):
    """
    Dependency to get the current user from the request's authorization header.
    This is a placeholder function and should be replaced with actual user retrieval logic.
    """
    try:
        if not authorization:
            raise TokenNotFoundError("Access denied, no access token provided")
        token = authorization.split(" ")[-1]

        AuthUtils.verify_token(token, auth_settings.access_token_public_key)
    except (TokenNotFoundError, jwt.InvalidTokenError) as e:
        logging.error(f"Token validation error: {str(e)}")
        raise e
    except Exception as e:
        logging.error(f"Authentication error: {str(e)}")
        raise e


async def get_refresh_token_repository(
    db: Annotated[DatabaseManager, Depends(get_db_manager)],
) -> IRefreshTokenRepository:
    conn = await db.get_connection()

    if db.initializer is None or conn is None:
        raise Exception("Database not initialized.")

    if db.db_type == DatabaseType.MONGODB:
        from repository.mongo.refresh_token_repository_mongodb import (
            RefreshTokenRepositoryMongoDB,
        )

        return RefreshTokenRepositoryMongoDB(conn)
    else:
        raise ValueError(
            f"Database type {db.db_type} is not supported for hotel repository."
        )


async def get_user_repository(
    db: Annotated[DatabaseManager, Depends(get_db_manager)],
) -> IUserRepository:
    conn = await db.get_connection()

    if db.initializer is None or conn is None:
        raise Exception("Database not initialized.")

    if db.db_type == DatabaseType.MONGODB:
        from repository.mongo.user_repository_mongodb import UserRepositoryMongoDB

        return UserRepositoryMongoDB(conn)
    else:
        raise ValueError(
            f"Database type {db.db_type} is not supported for user repository."
        )


def get_user_service(
    auth_settings: Annotated[AuthSettings, Depends(get_auth_settings)],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
    refresh_token_repository: Annotated[
        IRefreshTokenRepository, Depends(get_refresh_token_repository)
    ],
) -> UserService:
    return UserService(auth_settings, user_repository, refresh_token_repository)


async def get_hotel_repository(
    db: Annotated[DatabaseManager, Depends(get_db_manager)],
) -> IHotelRepository:
    conn = await db.get_connection()

    if db.initializer is None or conn is None:
        raise Exception("Database not initialized.")

    if db.db_type == DatabaseType.MONGODB:
        from repository.mongo.hotel_repository_mongodb import HotelRepositoryMongoDB

        return HotelRepositoryMongoDB(conn)
    else:
        raise ValueError(
            f"Database type {db.db_type} is not supported for hotel repository."
        )


def get_hotel_service(
    hotel_repository: Annotated[IHotelRepository, Depends(get_hotel_repository)],
) -> HotelService:
    return HotelService(hotel_repository)


async def get_booking_repository(
    db: Annotated[DatabaseManager, Depends(get_db_manager)],
) -> IBookingRepository:
    conn = await db.get_connection()

    if db.initializer is None or conn is None:
        raise Exception("Database not initialized.")

    if db.db_type == DatabaseType.MONGODB:
        from repository.mongo.booking_repository_mongodb import BookingRepositoryMongoDB

        return BookingRepositoryMongoDB(conn)
    else:
        raise ValueError(
            f"Database type {db.db_type} is not supported for booking repository."
        )


def get_booking_service(
    booking_repository: Annotated[IBookingRepository, Depends(get_booking_repository)],
    hotel_repository: Annotated[IHotelRepository, Depends(get_hotel_repository)],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
) -> BookingService:
    return BookingService(booking_repository, hotel_repository, user_repository)
