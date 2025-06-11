from models.user import User
from typing import Optional
from pydantic import BaseModel
from pydantic import ConfigDict


class UserUpdateResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    is_updated: bool
    data: Optional[User] = None
    error: Optional[str] = None
