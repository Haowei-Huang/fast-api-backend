from typing import Annotated
from fastapi import APIRouter, Depends
from dependencies.dependencies import get_hotel_service
from models.hotel import Hotel
from schemas.hotel.response.hotel_get_response import HotelGetResponse
from schemas.hotel.response.hotel_list_response import HotelListResponse
from schemas.hotel.response.hotel_update_response import HotelUpdateResponse
from schemas.hotel.request.hotel_request import HotelRequest
from service.hotel_service import HotelService

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("/findAllHotels", response_model=HotelListResponse)
async def find_all_hotels(
    hotel_service: Annotated[HotelService, Depends(get_hotel_service)],
):
    return await hotel_service.find_all()


@router.get("/findHotelById/{hotel_id}", response_model=HotelGetResponse)
async def find_hotel_by_id(
    hotel_id: str, hotel_service: Annotated[HotelService, Depends(get_hotel_service)]
):
    return await hotel_service.get_by_id(hotel_id)


@router.put("/updateHotel/{hotel_id}", response_model=HotelUpdateResponse)
async def update_hotel(
    hotel_id: str,
    req: HotelRequest,
    hotel_service: Annotated[HotelService, Depends(get_hotel_service)],
):
    return await hotel_service.update(hotel_id, req)


@router.get("/getUserBookedHotels/{user_id}", response_model=HotelListResponse)
async def get_user_booked_hotels(
    user_id: str,
    hotel_service: Annotated[HotelService, Depends(get_hotel_service)],
):
    return await hotel_service.get_hotels_by_user_id(user_id)
