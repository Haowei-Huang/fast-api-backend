from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class AuthSetting(BaseSettings):
    access_token_public_key: str = os.environ.get("ACCESS_PUBLIC_KEY")
    access_token_private_key: str = os.environ.get("ACCESS_PRIVATE_KEY")
    refresh_token_public_key: str = os.environ.get("REFRESH_PUBLIC_KEY")
    refresh_token_private_key: str = os.environ.get("REFRESH_PRIVATE_KEY")
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = 15
