from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from config.py_object_id import PyObjectId
from .user_role import UserRole
from typing import Optional
from models.address import Address
from pydantic import ConfigDict


class ClientInfo(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_by_alias=True,
        validate_by_name=True,
        arbitrary_types_allowed=True,
    )

    first_name: str = Field(
        ..., alias="firstName", pattern="^[a-zA-Z ,.'-]+$", max_length=20
    )
    last_name: str = Field(
        ..., alias="lastName", pattern="^[a-zA-Z ,.'-]+$", max_length=20
    )
    email: EmailStr
    phone: str = Field(..., pattern="^[0-9]{10}$")


class CardInfo(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_by_alias=True,
        validate_by_name=True,
        arbitrary_types_allowed=True,
    )

    card_number: str = Field(..., pattern="^[0-9]{16}$", alias="cardNumber")
    card_holder: str = Field(
        ..., alias="cardName", pattern="^[a-zA-Z ,.'-]+$", max_length=50
    )
    expiration_date: str = Field(
        ..., pattern="^(0[1-9]|1[012])[0-9]{2}$", alias="expDate"
    )
    cvv: str = Field(..., pattern="^[0-9]{3}$")
    address: Address


class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
        # json_encoders={ObjectId: lambda v: str(v)},  # for ObjectId serialization
        validate_by_alias=True,
        validate_by_name=True,
        arbitrary_types_allowed=True,
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    email: EmailStr
    role: UserRole
    password: str = Field(..., min_length=8)
    is_active: bool = Field(default=True, alias="isActive")
    client_info: Optional[ClientInfo] = Field(default=None, alias="clientInfo")
    card_info: Optional[CardInfo] = Field(default=None, alias="cardInfo")
