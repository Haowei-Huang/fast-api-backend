from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from models.address import Address
from bson import ObjectId

BaseModel.model_config["json_encoders"] = {ObjectId: lambda v: str(v)}


class Room(BaseModel):
    description: str
    is_active: bool = Field(default=True, alias="isActive")
    type: str
    baseRate: float
    bedOptions: str
    sleep_count: int = Field(..., alias="sleepCount")
    tags: List[str]
    room_id: str = Field(..., alias="roomId")


class Hotel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    hotel_name: str = Field(..., alias="hotelName")
    is_active: bool = Field(default=True, alias="isActive")
    description: str
    tags: List[str]
    photo_url: str = Field(..., alias="photo")
    rating: float = Field(..., alias="rating")
    address: Address
