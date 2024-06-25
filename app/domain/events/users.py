from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class UserCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New User Created"

    username: str
    user_oid: str
    phone: str


@dataclass
class UserDeletedEvent(BaseEvent):
    title: ClassVar[str] = "User was deleted"

    user_oid: str
    username: str
    phone: str