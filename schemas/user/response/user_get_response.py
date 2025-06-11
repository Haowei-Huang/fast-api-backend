from typing import Optional
from pydantic import BaseModel
from models.user import User
from bson import ObjectId
from pydantic import ConfigDict


class UserGetResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    data: Optional[User] = None
    error: Optional[str] = None
