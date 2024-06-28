from dataclasses import field, dataclass
from datetime import UTC, datetime

from domain.entities.base import BaseEntity
from domain.exceptions.users import UserAlreadyDeleted, UsernameAlreadyExists
from domain.values.users import Username, Phone, Password
from domain.events.users import (
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

    existing_usernames: list[Username] = field(default_factory=list)

    @classmethod
    async def create(
        cls,
        username: Username,
        password: Password,
        phone: Phone,
        existing_usernames: list[Username],
    ) -> "UserEntity":
        # TODO define why username is unhashable
        if username in existing_usernames:
            raise UsernameAlreadyExists(username.as_generic_type())
        existing_usernames.append(username)

        new_user = cls(
            phone=phone,
            username=username,
            password=password,
            existing_usernames=existing_usernames,
        )
        new_user.register_event(
            UserCreatedEvent(
                username=new_user.username.as_generic_type(),
                phone=new_user.phone.as_generic_type(),
                user_oid=new_user.oid,
            )
        )
        return new_user

    async def change_username(
        self, new_username: Username, existing_usernames=list[Username]
    ) -> None:
        self._validate_not_deleted()

        old_username = self.username.as_generic_type()
        if new_username != self.username:
            if new_username in existing_usernames:
                raise UsernameAlreadyExists(new_username.as_generic_type())

            # TODO change existing_usernames defining by creating converter to dto
            self.existing_usernames = existing_usernames
            self.existing_usernames.remove(self.username)
            self.existing_usernames.append(new_username)
            self.username = new_username

        self.register_event(
            UserChangedUsernameEvent(
                user_oid=self.oid,
                old_username=old_username,
                new_username=new_username.as_generic_type(),
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
