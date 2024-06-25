from dataclasses import dataclass

from logic.exceptions.base import LogicException
from http import HTTPStatus


@dataclass(eq=False)
class UserAlreadyExistsException(LogicException):
    @property
    def message(self) -> str:
        return "User already exists"

    @property
    def status_code(self) -> int:
        return HTTPStatus.CONFLICT.value


@dataclass(eq=False)
class UserNotFoundException(LogicException):
    value: str

    @property
    def message(self) -> str:
        return f"User with {self.value=} was not found"

    @property
    def status_code(self) -> int:
        return HTTPStatus.NOT_FOUND.value


@dataclass(eq=False)
class InvalidCredentialsException(LogicException):
    @property
    def message(self) -> str:
        return "Invalid credentials were provided"

    @property
    def status_code(self) -> int:
        return HTTPStatus.UNAUTHORIZED.value
