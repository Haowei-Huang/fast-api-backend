from ..user_repository import IUserRepository
from typing import Optional
from models.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from config.py_object_id import PyObjectId


class UserRepositoryMongoDB(IUserRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.user_collection = db.get_collection("users")

    async def get_by_email(self, email: str) -> Optional[User]:
        user = await self.user_collection.find_one({"email": email})
        # need to convert raw documents to User instance
        if user:
            return User(**user)
        return None

    async def get_by_id(self, user_id: str) -> Optional[User]:
        user = await self.user_collection.find_one(
            {"_id": ObjectId(user_id)}  # must convert str to ObjectId
        )
        # need to convert raw documents to User instance
        if user:
            return User(**user)
        return None

    async def create_user(self, user: User) -> Optional[PyObjectId]:
        response = await self.user_collection.insert_one(
            user.model_dump(by_alias=True, exclude_unset=True)
        )
        return response.inserted_id

    async def find_all(self) -> list[User]:
        raw_documents = await self.user_collection.find().to_list(100)
        if raw_documents:
            users = [User(**doc) for doc in raw_documents]
            return users
        return []

    async def delete(self, user_id: str):
        response = await self.user_collection.delete_one({"_id": ObjectId(user_id)})
        return response.deleted_count

    async def update(self, user_id: str, user_data: User) -> int:
        response = await self.user_collection.replace_one(
            {"_id": ObjectId(user_id)},
            user_data.model_dump(by_alias=True, exclude_unset=True),
        )
        return response.modified_count
