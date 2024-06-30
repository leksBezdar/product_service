from dataclasses import field, dataclass
from datetime import UTC, datetime

from domain.entities.base import BaseEntity
from domain.exceptions.users import UserAlreadyDeleted
from domain.values.users import Username, Phone, Password
from domain.events.users import (
    UserChangedPasswordEvent,
    UserChangedUsernameEvent,
    UserCreatedEvent,
    UserDeletedEvent,
)


@dataclass(eq=False)
class UserEntity(BaseEntity):
    phone: Phone
    username: Username
    password: Password
    is_verified: bool = field(default=False, kw_only=True)
    deleted_at: datetime | None = field(default=None, kw_only=True)

    @classmethod
    async def create(
        cls,
        username: Username,
        password: Password,
        phone: Phone,
    ) -> "UserEntity":
        # TODO define why username is unhashable

        new_user = cls(
            phone=phone,
            username=username,
            password=password,
        )
        new_user.register_event(
            UserCreatedEvent(
                username=new_user.username.as_generic_type(),
                phone=new_user.phone.as_generic_type(),
                user_oid=new_user.oid,
            )
        )
        return new_user

    async def change_username(self, new_username: Username) -> None:
        self._validate_not_deleted()
        old_username = self.username
        self.username = new_username

        self.register_event(
            UserChangedUsernameEvent(
                user_oid=self.oid,
                old_username=old_username,
                new_username=new_username,
            )
        )

    async def change_password(self, new_password: Password) -> None:
        self._validate_not_deleted()
        self.password = new_password

        self.register_event(
            UserChangedPasswordEvent(
                user_oid=self.oid,
            )
        )

    def delete(self) -> None:
        self._validate_not_deleted()
        self.deleted_at = datetime.now(UTC)

        self.register_event(
            UserDeletedEvent(
                user_oid=self.oid,
                username=self.username.as_generic_type(),
                phone=self.phone.as_generic_type(),
            )
        )

    def _validate_not_deleted(self) -> None:
        if self.deleted_at is not None:
            raise UserAlreadyDeleted(self.oid)
