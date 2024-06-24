from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class InvalidUsernameLength(ApplicationException):
    username_value: str

    @property
    def message(self) -> str:
        return f"Username length is invalid: {self.username_value}"


@dataclass(eq=False)
class EmptyUsername(ApplicationException):
    @property
    def message(self) -> str:
        return "Username is empty"


@dataclass(eq=False)
class EmptyPassword(ApplicationException):
    @property
    def message(self) -> str:
        return "Password is empty"


@dataclass(eq=False)
class InvalidPasswordLength(ApplicationException):
    length: str

    @property
    def message(self) -> str:
        return f"Password length is invalid: {self.length}"


@dataclass(eq=False)
class EmptyPhone(ApplicationException):
    @property
    def message(self) -> str:
        return "Phone is empty"


@dataclass(eq=False)
class InvalidPhone(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f"The provided phone is invalid: {self.email}"
