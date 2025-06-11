from typing import Optional
from pydantic import BaseModel, ConfigDict
from config.py_object_id import PyObjectId
from pydantic import Field
from bson import ObjectId


class BookingCreateResponse(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        arbitrary_types_allowed=True,
        # json_encoders={ObjectId: lambda v: str(v)},
    )

    is_created: bool
    data: Optional[PyObjectId] = None
    error: Optional[str] = None
