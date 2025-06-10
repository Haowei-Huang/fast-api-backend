from abc import ABC

from ..user_repository import IUserRepository
from typing import List, Optional
from models.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId


class UserRepositoryMongoDB(IUserRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.user_collection = db.get_collection("users")

    async def get_by_email(self, email: str) -> Optional[User]:
        user = await self.user_collection.find_one({"email": email})
        return User(**user) if user else None

    async def get_by_id(self, user_id: str) -> Optional[User]:
        user = await self.user_collection.find_one({"_id": ObjectId(user_id)})
        return User(**user) if user else None

    async def create_user(self, user: User) -> Optional[str]:
        response = await self.user_collection.insert_one(user.model_dump())
        return str(response.inserted_id)

    async def find_all(self) -> List[User]:
        raw_documents = await self.user_collection.find().to_list(None)
        return [User(**doc) for doc in raw_documents]

    async def delete(self, user_id: str) -> int:
        response = await self.user_collection.delete_one({"_id": ObjectId(user_id)})
        return response.deleted_count

    async def update(self, user_id: str, user_data: User) -> int:
        response = await self.user_collection.replace_one(
            {"_id": ObjectId(user_id)}, user_data.model_dump()
        )
        return response.modified_count
