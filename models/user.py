from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from .user_role import UserRole
from typing import List, Optional
from models.address import Address

BaseModel.model_config["json_encoders"] = {ObjectId: lambda v: str(v)}


class ClientInfo(BaseModel):
    first_name: str = Field(..., alias="firstName", pattern="^[a-zA-Z ,.'-]+$")
    last_name: str = Field(..., alias="lastName", pattern="^[a-zA-Z ,.'-]+$")
    email: EmailStr
    phone: str = Field(..., pattern="^[0-9]{10}$")


class CardInfo(BaseModel):
    card_number: str = Field(..., pattern="^[0-9]{16}$", alias="cardNumber")
    card_holder: str = Field(..., alias="cardName", pattern="^[a-zA-Z ,.'-]+$")
    expiration_date: str = Field(
        ..., pattern="^(0[1-9]|1[012])[0-9]{2}$", alias="expDate"
    )
    cvv: str = Field(..., pattern="^[0-9]{3}$")
    address: Address


def ensure_object_id(value) -> ObjectId:
    if not ObjectId.is_valid(value):
        return ObjectId(value)
    return value


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Optional[PydanticObjectId]
    email: EmailStr
    role: UserRole
    password: str = Field(..., min_length=8)
    is_active: bool = Field(default=True, alias="isActive")
    client_info: Optional[ClientInfo] = Field(default=None, alias="clientInfo")
    card_info: Optional[CardInfo] = Field(default=None, alias="cardInfo")

    class Config:
        use_enum_values = True  # use the value
