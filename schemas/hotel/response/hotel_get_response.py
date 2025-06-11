from typing import Optional
from pydantic import BaseModel
from models.hotel import Hotel
from bson import ObjectId
from pydantic import ConfigDict


class HotelGetResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    data: Optional[Hotel] = None
    error: Optional[str] = None
