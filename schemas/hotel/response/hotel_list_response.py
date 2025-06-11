from typing import Optional, Any, Dict
from pydantic import BaseModel
from models.hotel import Hotel
from bson import ObjectId
from pydantic import ConfigDict


class HotelListResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    data: list[Hotel] = []
    error: Optional[str] = None
