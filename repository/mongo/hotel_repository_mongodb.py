from ..hotel_repository import IHotelRepository
from typing import Optional
from models.hotel import Hotel
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from config.py_object_id import PyObjectId


class HotelRepositoryMongoDB(IHotelRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.hotel_collection = db.get_collection("hotels")
        self.booking_collection = db.get_collection("bookings")

    async def get_by_id(self, hotel_id: str) -> Optional[Hotel]:
        hotel = await self.hotel_collection.find_one(
            {"_id": ObjectId(hotel_id)}  # must convert str to ObjectId
        )
        # need to convert raw documents to Hotel instance
        if hotel:
            return Hotel(**hotel)
        return None

    async def find_all(self) -> list[Hotel]:
        raw_documents = await self.hotel_collection.find().to_list(100)
        if raw_documents:
            hotels = [Hotel(**doc) for doc in raw_documents]
            return hotels
        return []

    async def update(self, hotel_id: str, hotel_data: Hotel) -> int:
        response = await self.hotel_collection.replace_one(
            {"_id": ObjectId(hotel_id)},
            hotel_data.model_dump(by_alias=True, exclude_unset=True),
        )
        return response.modified_count

    async def get_hotels_by_user_id(self, user_id: str) -> list[Hotel]:
        pipeline = [
            {"$match": {"userId": user_id}},  # find by user
            {
                "$group": {"_id": "$hotel"}
            },  # group by hotel, hotel field in bookings is the '_id' in hotels
            {
                "$addFields": {
                    "hotelObjectId": {
                        "$toObjectId": "$_id"
                    }  # Convert hotel string ID to ObjectId
                }
            },
            {
                "$lookup": {
                    "from": "hotels",
                    "localField": "hotelObjectId",  # The hotel ID from the group step
                    "foreignField": "_id",  # hotelId in hotels collection
                    "as": "hotelData",
                }
            },
            {"$unwind": "$hotelData"},  # unwind the array created by lookup
            {
                "$replaceRoot": {"newRoot": "$hotelData"}
            },  # replace the root to only return hotel Data
        ]
        raw_documents = await self.booking_collection.aggregate(pipeline).to_list(
            length=None
        )
        if raw_documents:
            hotels = [Hotel(**doc) for doc in raw_documents]
            return hotels
        return []
