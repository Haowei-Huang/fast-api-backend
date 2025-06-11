from ..booking_repository import IBookingRepository
from typing import Optional
from models.booking import Booking
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from config.py_object_id import PyObjectId


class BookingRepositoryMongoDB(IBookingRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.booking_collection = db.get_collection("bookings")

    async def find_all(self) -> list[Booking]:
        raw_documents = await self.booking_collection.find().to_list(100)
        if raw_documents:
            bookings = [Booking(**doc) for doc in raw_documents]
            return bookings
        return []

    async def get_by_id(self, booking_id: str) -> Optional[Booking]:
        booking = await self.booking_collection.find_one(
            {"_id": ObjectId(booking_id)}  # must convert str to ObjectId
        )
        # need to convert raw documents to Booking instance
        if booking:
            return Booking(**booking)
        return None

    async def create_booking(self, booking: Booking) -> Optional[PyObjectId]:
        response = await self.booking_collection.insert_one(
            booking.model_dump(by_alias=True, exclude_unset=True)
        )
        return response.inserted_id

    async def get_bookings_by_user_id(self, user_id: str) -> list[Booking]:
        raw_documents = await self.booking_collection.find({"userId": user_id}).to_list(
            100
        )
        if raw_documents:
            bookings = [Booking(**doc) for doc in raw_documents]
            return bookings
        return []
