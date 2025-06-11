from abc import ABC, abstractmethod
from typing import Optional
from models.hotel import Hotel
from config.py_object_id import PyObjectId


class IHotelRepository(ABC):
    @abstractmethod
    async def get_by_id(self, hotel_id: str) -> Optional[Hotel]:
        pass

    @abstractmethod
    async def find_all(self) -> list[Hotel]:
        pass

    @abstractmethod
    async def update(self, hotel_id: str, hotel_data: Hotel) -> int:
        pass

    @abstractmethod
    async def get_hotels_by_user_id(self, user_id: str) -> list[Hotel]:
        pass
