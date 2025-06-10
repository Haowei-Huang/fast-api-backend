from config.database_manager import DatabaseManager
from config.settings import Settings
from typing import Annotated
from fastapi import Depends, Request
from config.database_manager import DatabaseType
from repository.user_repository import IUserRepository
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
