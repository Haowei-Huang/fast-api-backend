from abc import ABC, abstractmethod
from typing import Optional
from models.booking import Booking
from config.py_object_id import PyObjectId


class IBookingRepository(ABC):
    @abstractmethod
    async def find_all(self) -> list[Booking]:
        pass

    @abstractmethod
    async def get_by_id(self, booking_id: str) -> Optional[Booking]:
        pass

    @abstractmethod
    async def create_booking(self, booking: Booking) -> Optional[PyObjectId]:
        pass

    @abstractmethod
    async def get_bookings_by_user_id(self, user_id: str) -> list[Booking]:
        pass
