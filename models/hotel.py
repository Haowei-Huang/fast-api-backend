from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models.address import Address
from bson import ObjectId
from config.py_object_id import PyObjectId

BaseModel.model_config["json_encoders"] = {ObjectId: lambda v: str(v)}


class Room(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, validate_by_alias=True, validate_by_name=True
    )

    description: str = Field(..., max_length=50)
    is_active: bool = Field(default=True, alias="isActive")
    type: str = Field(..., max_length=20)
    base_rate: float = Field(..., alias="baseRate")
    bed_options: str = Field(..., max_length=20, alias="bedOptions")
    sleep_count: int = Field(..., alias="sleepsCount")
    tags: list[str]
    room_id: str = Field(alias="roomId", max_length=20)


class Hotel(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_by_alias=True,
        validate_by_name=True,
        arbitrary_types_allowed=True,
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    hotel_name: str = Field(alias="hotelName", max_length=50)
    is_active: bool = Field(default=True, alias="isActive")
    description: str = Field(..., max_length=500)
    tags: list[str]
    photo_url: str = Field(alias="photo")
    rating: float
    address: Address
    rooms: list[Room]
