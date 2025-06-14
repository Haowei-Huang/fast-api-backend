from abc import ABC, abstractmethod
from typing import Optional
from models.refresh_token_in_db import RefreshTokenInDB
from config.py_object_id import PyObjectId


class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[RefreshTokenInDB]:
        pass

    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[RefreshTokenInDB]:
        pass

    @abstractmethod
    async def create_refresh_token(
        self, tokenInDB: RefreshTokenInDB
    ) -> Optional[PyObjectId]:
        pass

    @abstractmethod
    async def delete(self, token: str):
        pass

    @abstractmethod
    async def update(self, token: str, newToken: str) -> int:
        pass
