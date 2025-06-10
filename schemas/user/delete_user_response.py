from models.user import User
from typing import Optional
from pydantic import BaseModel
from bson import ObjectId

BaseModel.model_config["json_encoders"] = {ObjectId: lambda v: str(v)}


class DeleteUserResponse(BaseModel):
    is_deleted: bool
    user_id: Optional[str]  # Optional[PydanticObjectId] = None
    error: Optional[str]
