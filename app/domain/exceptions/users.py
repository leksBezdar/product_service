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
class InvalidPhoneFormat(ApplicationException):
    phone: str

    @property
    def message(self) -> str:
        return f"The provided phone is invalid: {self.phone}"


@dataclass(eq=False)
class InvalidPhoneLength(ApplicationException):
    length: str

    @property
    def message(self) -> str:
        return f"Phone length is invalid: {self.length}"


@dataclass(eq=False)
class InvalidUsernameCharacters(ApplicationException):
    value: str

    @property
    def message(self) -> str:
        return f"The provided username has invalid characters: {self.value}"


@dataclass(eq=False)
class UserAlreadyDeleted(ApplicationException):
    value: str

    @property
    def message(self) -> str:
        return f"User with id {self.value} has already been deleted"


@dataclass(eq=False)
class UserNotDeleted(ApplicationException):
    value: str

    @property
    def message(self) -> str:
        return f"User with id {self.value} has not been deleted"
