import datetime
from passlib.context import CryptContext
import jwt
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO or DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format for log messages
)


class AuthUtils:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def get_hashed_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return AuthUtils.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password."""
        return AuthUtils.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def generate_access_token(
        data: dict,
        secret_key: str,
        algorithm: str = "RS256",
        expires_delta: datetime.timedelta | None = None,
    ) -> str:
        """Generate a JWT access token."""
        if not expires_delta:
            exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                seconds=10
            )
        else:
            exp = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        data.update({"exp": exp})
        return jwt.encode(payload=data, key=secret_key, algorithm=algorithm)

    @staticmethod
    def generate_refresh_token(
        data: dict,
        secret_key: str,
        algorithm: str = "RS256",
        expires_delta: datetime.timedelta | None = None,
    ) -> dict:
        """Generate a JWT refresh token."""
        logging.debug(f"Generating refresh token with data: {data}")
        if not expires_delta:
            exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                hours=1
            )
        else:
            exp = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        data.update({"exp": exp})
        return {
            "exp": exp,
            "token": jwt.encode(payload=data, key=secret_key, algorithm=algorithm),
        }

    @staticmethod
    def verify_token(
        token: str, secret_key: str, algorithms: list[str] = ["RS256"]
    ) -> dict:
        """Decode a JWT token."""
        try:
            return jwt.decode(
                token,
                key=secret_key,
                algorithms=algorithms,
                # leeway=datetime.timedelta(seconds=60),
                audience="simplii-book",
            )
        except jwt.ExpiredSignatureError as e:
            logging.error(f"Token has expired: {str(e)}")
            raise e
        except jwt.InvalidTokenError as e:
            logging.error(f"Invalid token: {str(e)}")
            raise e
