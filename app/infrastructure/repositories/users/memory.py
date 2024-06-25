from dataclasses import dataclass, field
from typing import Iterable

from domain.entities.users import UserEntity
from infrastructure.repositories.users.base import IUserRepository
from infrastructure.repositories.users.filters.users import GetUsersFilters


@dataclass
class InMemoryUserRepository(IUserRepository):
    _saved_users: list[UserEntity] = field(default_factory=list, kw_only=True)

    async def add_user(self, user: UserEntity) -> None:
        self._saved_users.append(user)

    async def get_by_oid(self, user_oid: str) -> UserEntity | None:
        for user in self._saved_users:
            if user.oid == user_oid:
                return user
        return None

    async def get_all(
        self, filters: GetUsersFilters
    ) -> tuple[Iterable[UserEntity], int]:
        total_count = len(self._saved_users)
        limited_users = self._saved_users[
            filters.offset : filters.offset + filters.limit
        ]
        return limited_users, total_count

    async def delete(self, user_oid: str) -> UserEntity | None:
        for user in self._saved_users:
            if user.oid == user_oid:
                self._saved_users.remove(user)
                return user
        return None

    async def check_user_exists_by_phone_and_username(
        self, phone: str, username: str
    ) -> bool:
        return any(
            user.phone.as_generic_type() == phone
            or user.username.as_generic_type() == username
            for user in self._saved_users
        )
