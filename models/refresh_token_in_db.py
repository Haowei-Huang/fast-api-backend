from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
import datetime
from bson import ObjectId
from config.py_object_id import PyObjectId


class RefreshTokenInDB(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_by_alias=True,
        validate_by_name=True,
        arbitrary_types_allowed=True,
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId = Field(..., alias="userId")
    token: str
    created_at: datetime.datetime = Field(..., alias="createdAt")
    expired_at: datetime.datetime = Field(..., alias="expiredAt")
