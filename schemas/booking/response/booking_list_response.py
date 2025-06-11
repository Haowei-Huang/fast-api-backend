from typing import Optional
from pydantic import BaseModel
from models.booking import Booking
from bson import ObjectId
from pydantic import ConfigDict


class BookingListResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    data: list[Booking] = []
    error: Optional[str] = None
