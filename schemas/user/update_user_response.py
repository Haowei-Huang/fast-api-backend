from models.user import User
from typing import Optional
from pydantic import BaseModel

class UpdateUserResponse(BaseModel):
    is_updated: bool
    data: Optional[User]
    error: Optional[str]