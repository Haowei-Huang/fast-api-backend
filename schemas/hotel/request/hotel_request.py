from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from config.py_object_id import PyObjectId
from bson import ObjectId
from models.address import Address
from models.hotel import Room


class HotelRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_by_alias=True,
        validate_by_name=True,
        arbitrary_types_allowed=True,
    )

    hotel_name: str = Field(alias="hotelName", max_length=50)
    is_active: bool = Field(default=True, alias="isActive")
    description: str = Field(..., max_length=500)
    tags: list[str]
    photo_url: str = Field(alias="photo")
    rating: float
    address: Address
    rooms: list[Room]
