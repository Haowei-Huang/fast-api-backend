from abc import ABC, abstractmethod
from typing import List, Optional
from models.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> Optional[str]:
        pass

    @abstractmethod
    async def find_all(self) -> List[User]:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> str:
        pass

    @abstractmethod
    async def update(self, user_id: str, user_data: User) -> Optional[User]:
        pass
