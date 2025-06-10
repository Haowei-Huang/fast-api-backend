from typing import Optional
from pydantic import BaseModel
from bson import ObjectId

BaseModel.model_config["json_encoders"] = {ObjectId: lambda v: str(v)}


class CreateUserResponse(BaseModel):
    is_created: bool
    data: Optional[str]  # Optional[PydanticObjectId] = None
    error: Optional[str]
