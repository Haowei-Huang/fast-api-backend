from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from config.py_object_id import PyObjectId
from models.user_role import UserRole
from bson import ObjectId
from models.user import ClientInfo
from models.user import CardInfo


class UserRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
        validate_by_alias=True,
        validate_by_name=True,
        arbitrary_types_allowed=True,
    )

    email: EmailStr
    role: UserRole
    password: str = Field(..., min_length=8)
    is_active: bool = Field(default=True, alias="isActive")
    client_info: Optional[ClientInfo] = Field(default=None, alias="clientInfo")
    card_info: Optional[CardInfo] = Field(default=None, alias="cardInfo")
