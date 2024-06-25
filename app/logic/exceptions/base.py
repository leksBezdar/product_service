from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class LogicException(ApplicationException):
    @property
    def message(self) -> str:
        return "Logic exeption has occurred"
