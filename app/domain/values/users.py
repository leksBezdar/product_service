from dataclasses import dataclass

from domain.exceptions.users import (
    EmptyPhone,
    EmptyPassword,
    EmptyUsername,
    InvalidPasswordLength,
    InvalidUsernameLength,
)
from domain.values.base import BaseValueObject


@dataclass
class Username(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyUsername()

        value_length = len(self.value)

        if value_length not in range(3, 16):
            raise InvalidUsernameLength(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class Phone(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyPhone()

    def as_generic_type(self):
        return str(self.value)


@dataclass
class Password(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyPassword()

        value_length = len(self.value)

        if value_length not in range(3, 100):
            raise InvalidPasswordLength(value_length)

    def as_generic_type(self):
        return str(self.value)
