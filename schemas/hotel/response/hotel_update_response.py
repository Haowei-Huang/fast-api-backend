from models.hotel import Hotel
from typing import Optional
from pydantic import BaseModel
from pydantic import ConfigDict


class HotelUpdateResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    is_updated: bool
    data: Optional[Hotel] = None
    error: Optional[str] = None
