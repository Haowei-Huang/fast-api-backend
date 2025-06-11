from config.database_manager import DatabaseManager
from config.settings import Settings
from typing import Annotated
from fastapi import Depends, Request
from config.database_manager import DatabaseType
from repository.booking_repository import IBookingRepository
from repository.hotel_repository import IHotelRepository
from repository.user_repository import IUserRepository
from service.booking_service import BookingService
from service.hotel_service import HotelService
from service.user_service import UserService


def get_settings() -> Settings:
    return Settings()


def get_db_manager(request: Request) -> DatabaseManager:
    return request.app.state.db_manager


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
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(user_repository)


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
