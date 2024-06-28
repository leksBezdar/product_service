from dataclasses import dataclass
import hashlib
import re

from domain.exceptions.users import (
    EmptyPhone,
    EmptyPassword,
    EmptyUsername,
    InvalidPasswordLength,
    InvalidPhoneLength,
    InvalidUsernameCharacters,
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

        if not re.match(r"^[a-zA-Z0-9_*\\-]+$", self.value):
            raise InvalidUsernameCharacters(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class Phone(BaseValueObject):
    value: str

    def __post_init__(self) -> None:
        self.format_to_digits_only()
        super().__post_init__()

    def format_to_digits_only(self) -> None:
        digits_only = re.sub(r"\D", "", self.value)
        self.value = f"+{digits_only}"

    def validate(self):
        if not self.value:
            raise EmptyPhone()

        phone_length = len(self.value)
        if phone_length not in range(8, 65):
            raise InvalidPhoneLength(phone_length)

    def as_generic_type(self):
        return str(self.value)


@dataclass
class Password(BaseValueObject):
    value: str
    __is_hashed: bool = False

    def __post_init__(self):
        super().__post_init__()
        self.hash_password(self.value)

    def validate(self):
        if not self.value:
            raise EmptyPassword()

        value_length = len(self.value)

        if value_length not in range(3, 100):
            raise InvalidPasswordLength(value_length)

    def hash_password(self, password: str) -> str:
        if not self.__is_hashed:
            self.value = hashlib.sha256(password.encode()).hexdigest()
            self.__is_hashed = True

    def as_generic_type(self):
        return str(self.value)
