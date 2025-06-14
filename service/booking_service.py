from bson import ObjectId
from repository.booking_repository import IBookingRepository
from repository.hotel_repository import IHotelRepository
from repository.user_repository import IUserRepository
from models.booking import Booking
import inspect
import logging
from schemas.booking.response.booking_create_response import BookingCreateResponse
from schemas.booking.response.booking_list_response import BookingListResponse
from schemas.booking.request.booking_request import BookingRequest
from passlib.context import CryptContext
from exceptions.custom_exception import (
    BookingServiceError,
    HotelNotFoundError,
    NotFoundError,
    UserNotFoundError,
)
from exceptions.user_identifier import UserIdentifier

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO or DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format for log messages
)


class BookingService:
    def __init__(
        self,
        booking_repository: IBookingRepository,
        hotel_repository: IHotelRepository,
        user_repository: IUserRepository,
    ):
        self.booking_repository = booking_repository
        self.hotel_repository = hotel_repository
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def find_all(self) -> BookingListResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            bookings = await self.booking_repository.find_all()
            return BookingListResponse(data=bookings, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise BookingServiceError(f"Failed to retrieve bookings: {str(e)}")
            # return BookingListResponse(data=[], error=str(e))

    async def create_booking(self, req: BookingRequest) -> BookingCreateResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")

            # check if hotel exists
            hotel = await self.hotel_repository.get_by_id(req.hotel_id)
            if not hotel:
                raise HotelNotFoundError(f"Hotel with id {req.hotel_id} does not exist")

            # check if user exists if user_id is not empty
            if req.user_id:
                user = await self.user_repository.get_by_id(req.user_id)
                if not user:
                    raise UserNotFoundError(
                        UserIdentifier.user_id,
                        f"User with id {req.user_id} does not exist",
                    )

            booking = Booking(**req.model_dump(by_alias=True, exclude_unset=True))
            inserted_id = await self.booking_repository.create_booking(booking)

            if not inserted_id:
                raise BookingServiceError()

            # verify creation
            created_booking = await self.booking_repository.get_by_id(inserted_id)
            if not created_booking:
                raise BookingServiceError()

            return BookingCreateResponse(is_created=True, data=inserted_id, error=None)
        except NotFoundError as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise e
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise BookingServiceError(f"Failed to create booking: {str(e)}")
            # return BookingCreateResponse(is_created=False, data=None, error=str(e))

    async def get_bookings_by_user_id(self, user_id: str) -> BookingListResponse:
        try:
            logging.info(f"{inspect.stack()[1][3]} called")
            bookings = await self.booking_repository.get_bookings_by_user_id(user_id)
            return BookingListResponse(data=bookings, error=None)
        except Exception as e:
            logging.error(f"error in {inspect.stack()[1][3]}: ", exc_info=True)
            raise BookingServiceError(
                f"Failed to retrieve bookings for user {user_id}: {str(e)}"
            )
            # return BookingListResponse(data=[], error=str(e))
