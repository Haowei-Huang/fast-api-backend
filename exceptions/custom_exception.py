from exceptions.user_identifier import UserIdentifier


class NotFoundError(Exception):
    pass


class UserServiceError(Exception):
    """Base exception for user service errors"""

    pass


class UserAlreadyExistsError(UserServiceError):
    """Raised when trying to create a user that already exists"""

    pass


class UserNotFoundError(UserServiceError, NotFoundError):
    """Raised when a user cannot be found in the database."""

    def __init__(
        self, identifier: UserIdentifier, value: str
    ):  # identifier can be 'id' or 'email'
        super().__init__(f"User with {identifier.value} {value} not found")
        self.identifier = identifier
        self.value = value


class AuthenticationError(UserServiceError):
    pass


class TokenNotFoundError(AuthenticationError, NotFoundError):
    """Raised when a token cannot be found in the header or database"""

    pass


class WrongCredentialsError(AuthenticationError):
    """Raised when login credentials are incorrect"""

    pass


class HotelServiceError(Exception):
    pass


class HotelNotFoundError(HotelServiceError, NotFoundError):
    """Raised when a hotel cannot be found in the database."""


class BookingServiceError(Exception):
    pass
