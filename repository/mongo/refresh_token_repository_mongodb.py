from abc import ABC, abstractmethod
from typing import Optional

from bson import ObjectId
from models.refresh_token_in_db import RefreshTokenInDB
from repository.refresh_token_repository import IRefreshTokenRepository
from config.py_object_id import PyObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import datetime


class RefreshTokenRepositoryMongoDB(IRefreshTokenRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.refresh_token_collection = db.get_collection("refreshTokens")

    async def get_by_id(self, token_id: str) -> Optional[RefreshTokenInDB]:
        token = await self.refresh_token_collection.find_one(
            {"_id": ObjectId(token_id)}  # must convert str to ObjectId
        )
        # need to convert raw documents to User instance
        if token:
            return RefreshTokenInDB(**token)
        return None

    async def get_by_token(self, token: str) -> Optional[RefreshTokenInDB]:
        tokenInDB = await self.refresh_token_collection.find_one(
            {"token": token}  # must convert str to ObjectId
        )
        # need to convert raw documents to Hotel instance
        if tokenInDB:
            return RefreshTokenInDB(**tokenInDB)
        return None

    async def create_refresh_token(
        self, tokenInDB: RefreshTokenInDB
    ) -> Optional[PyObjectId]:
        response = await self.refresh_token_collection.insert_one(
            tokenInDB.model_dump(by_alias=True, exclude_unset=True)
        )
        return response.inserted_id

    async def delete(self, token: str):
        response = await self.refresh_token_collection.delete_one({"token": token})
        return response.deleted_count

    async def update(self, token: str, newToken: str) -> int:
        current_time = datetime.datetime.now()
        time_delta = datetime.timedelta(hours=1)
        response = await self.refresh_token_collection.update_one(
            {"token": token},
            {
                "$set": {
                    "token": newToken,
                    "createdAt": current_time,
                    "expiredAt": current_time + time_delta,
                }
            },
        )
        return response.modified_count
