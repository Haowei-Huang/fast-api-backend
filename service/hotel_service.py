from bson import ObjectId
from repository.hotel_repository import IHotelRepository
from models.hotel import Hotel
import inspect
import logging
from fastapi.encoders import jsonable_encoder
from schemas.hotel.response.hotel_list_response import HotelListResponse
from schemas.hotel.response.hotel_get_response import HotelGetResponse
from schemas.hotel.response.hotel_update_response import HotelUpdateResponse
from schemas.hotel.request.hotel_request import HotelRequest
from exceptions.custom_exception import HotelUpdateError
from passlib.context import CryptContext


class HotelService:
    def __init__(
        self,
        hotel_repository: IHotelRepository,
    ):
        self.hotel_repository = hotel_repository

    async def find_all(self) -> HotelListResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            hotels = await self.hotel_repository.find_all()
            return HotelListResponse(data=hotels, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return HotelListResponse(data=[], error=str(e))

    async def get_by_id(self, hotel_id: str) -> HotelGetResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            hotel = await self.hotel_repository.get_by_id(hotel_id)
            return HotelGetResponse(data=hotel, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return HotelGetResponse(data=None, error=str(e))

    async def update(self, hotel_id: str, req: HotelRequest) -> HotelUpdateResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            hotel = Hotel(**req.model_dump(by_alias=True, exclude_unset=True))

            modified_count = await self.hotel_repository.update(hotel_id, hotel)
            if modified_count != 1:
                raise HotelUpdateError(f"Failed to update hotel with id {hotel_id}")

            updated_hotel = await self.hotel_repository.get_by_id(hotel_id)
            return HotelUpdateResponse(is_updated=True, data=updated_hotel, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return HotelUpdateResponse(is_updated=False, data=None, error=str(e))

    async def get_hotels_by_user_id(self, user_id: str) -> HotelListResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            hotels = await self.hotel_repository.get_hotels_by_user_id(user_id)
            return HotelListResponse(data=hotels, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            return HotelListResponse(data=[], error=str(e))
