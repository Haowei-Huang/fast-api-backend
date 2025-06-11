from pydantic import BaseModel, Field
from typing import Optional
from config.py_object_id import PyObjectId
import datetime
from models.user import ClientInfo, CardInfo


class Booking(BaseModel):
    model_config = {
        "str_strip_whitespace": True,
        "validate_by_alias": True,
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
    }

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    hotel_id: PyObjectId = Field(alias="hotel")
    start_date: datetime.datetime = Field(alias="from")
    end_date: datetime.datetime = Field(alias="to")
    duration: int = Field(..., ge=1)
    number_of_guest: int = Field(alias="numberOfGuest", ge=1)
    rooms: list[str]
    total_price: float = Field(alias="totalPrice", ge=0)
    client_info: ClientInfo = Field(alias="clientInfo")
    card_info: CardInfo = Field(alias="cardInfo")
    user_id: PyObjectId = Field(default="", alias="userId")
    created_time: datetime.datetime = Field(alias="time")
