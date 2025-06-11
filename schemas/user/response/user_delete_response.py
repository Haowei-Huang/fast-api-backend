from config.py_object_id import PyObjectId
from models.user import User
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from bson import ObjectId


class UserDeleteResponse(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        arbitrary_types_allowed=True,
        # json_encoders={ObjectId: lambda v: str(v)},
    )

    is_deleted: bool
    user_id: Optional[PyObjectId] = None
    error: Optional[str] = None
