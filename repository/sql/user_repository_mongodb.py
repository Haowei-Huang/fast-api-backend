from abc import ABC
from ..user_repository import IUserRepository
from typing import List, Optional
from models.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase

class UserRepositorySQL(IUserRepository):
    def __init__(self, db):
        pass

    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    async def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    async def create_user(self, user: User) -> Optional[str]:
        pass

    async def find_all(self) -> List[User]:
        pass

    async def delete(self, user_id: str) -> int:
        pass

    async def update(self, user_id: str, user_data: User) -> int:
        pass