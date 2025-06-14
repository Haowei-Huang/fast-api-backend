from pydantic import BaseModel, ConfigDict
from typing import Optional
from models.user import User


class LoginResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    message: str
    user: Optional[User] = None
    token: Optional[str] = None
    error: Optional[str] = None
