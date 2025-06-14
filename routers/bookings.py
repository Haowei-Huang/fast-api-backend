from typing import Annotated
from fastapi import APIRouter, Depends
from dependencies.dependencies import get_booking_service, get_current_user
from models.booking import Booking
from schemas.booking.response.booking_create_response import BookingCreateResponse
from schemas.booking.response.booking_list_response import BookingListResponse
from schemas.booking.request.booking_request import BookingRequest
from service.booking_service import BookingService

router = APIRouter(prefix="/booking", tags=["bookings"])


@router.post("/createBooking", response_model=BookingCreateResponse)
async def create_booking(
    req: BookingRequest,
    booking_service: Annotated[BookingService, Depends(get_booking_service)],
):
    return await booking_service.create_booking(req)


@router.get(
    "/findAllBookings",
    dependencies=[Depends(get_current_user)],
    response_model=BookingListResponse,
)
async def find_all_bookings(
    booking_service: Annotated[BookingService, Depends(get_booking_service)],
):
    return await booking_service.find_all()


@router.get(
    "/findBookingByUserId/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=BookingListResponse,
)
async def get_bookings_by_user_id(
    user_id: str,
    booking_service: Annotated[BookingService, Depends(get_booking_service)],
):
    return await booking_service.get_bookings_by_user_id(user_id)
