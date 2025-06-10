from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
import datetime
from bson import ObjectId

BaseModel.model_config["json_encoders"] = {ObjectId: lambda v: str(v)}


class RefreshToken(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str = Field(..., alias="userId")
    token: str
    created_at: datetime.datetime = Field(..., alias="createdAt")
    expired_at: datetime.datetime = Field(..., alias="expiredAt")
