from dataclasses import dataclass

from logic.exceptions.base import LogicException
from http import HTTPStatus


@dataclass(eq=False)
class GroupAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self) -> str:
        return f"Group with that title already exists: {self.title}"

    @property
    def status_code(self) -> int:
        return HTTPStatus.CONFLICT.value


@dataclass(eq=False)
class GroupNotFoundException(LogicException):
    oid: str

    @property
    def message(self) -> str:
        return f"Group with {self.oid=} was not found"

    @property
    def status_code(self) -> int:
        return HTTPStatus.NOT_FOUND.value
