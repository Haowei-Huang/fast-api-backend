from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
import base64


class AuthSettings(BaseSettings):
    load_dotenv()
    access_token_public_key: str = base64.b64decode(
        os.environ.get("ACCESS_PUBLIC_KEY", "")
    ).decode("utf-8")
    access_token_private_key: str = base64.b64decode(
        os.environ.get("ACCESS_PRIVATE_KEY", "")
    ).decode("utf-8")
    refresh_token_public_key: str = base64.b64decode(
        os.environ.get("REFRESH_PUBLIC_KEY", "")
    ).decode("utf-8")
    refresh_token_private_key: str = base64.b64decode(
        os.environ.get("REFRESH_PRIVATE_KEY", "")
    ).decode("utf-8")
    algorithm: str = os.environ.get("ALGORITHM", "RS256")
    access_token_expire_minutes: int = 15
