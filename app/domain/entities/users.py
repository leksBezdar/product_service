from dataclasses import field, dataclass

from domain.entities.base import BaseEntity
from domain.values.users import Username, Phone, Password
from domain.events.users import (
    UserCreatedEvent,
    UserDeletedEvent,
)


@dataclass(eq=False)
class UserEntity(BaseEntity):
    phone: Phone
    username: Username
    password: Password
    is_verified: bool = field(default=False, kw_only=True)

    @classmethod
    async def create(
        cls, username: Username, password: Password, phone: Phone
    ) -> "UserEntity":
        new_user = cls(phone=phone, username=username, password=password)
        new_user.register_event(
            UserCreatedEvent(
                username=new_user.username.as_generic_type(),
                phone=new_user.phone.as_generic_type(),
                user_oid=new_user.oid,
            )
        )
        return new_user

    def delete(self) -> None:
        self.register_event(
            UserDeletedEvent(
                user_oid=self.oid,
                username=self.username.as_generic_type(),
                phone=self.phone.as_generic_type(),
            )
        )
