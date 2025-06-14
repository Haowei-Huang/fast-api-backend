from pydantic import BaseModel, ConfigDict
from typing import Optional


class RefreshTokenResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, arbitrary_types_allowed=True)

    message: str
    token: Optional[str] = None
    error: Optional[str] = None
