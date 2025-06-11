from typing import Optional, Any, Dict
from pydantic import BaseModel
from models.user import User
from bson import ObjectId
from pydantic import ConfigDict


class UserListResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    data: list[User] = []
    error: Optional[str] = None
