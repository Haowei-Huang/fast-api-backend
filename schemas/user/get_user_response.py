from typing import Optional, List
from pydantic import BaseModel
from models.user import User

class GetUserResponse(BaseModel):
    data: Optional[User|List[User]]
    error: Optional[str]