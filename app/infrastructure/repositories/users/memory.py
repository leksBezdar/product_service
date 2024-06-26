from dataclasses import dataclass, field
from typing import Iterable

from infrastructure.models.users import UserModel
from infrastructure.repositories.users.base import IUserRepository
from infrastructure.repositories.users.filters.users import GetUsersFilters


@dataclass
class InMemoryUserRepository(IUserRepository):
    _saved_users: list[UserEntity] = field(default_factory=list, kw_only=True)

    async def add_user(self, user: UserModel) -> None:
        self._saved_users.append(user)

    async def get_by_oid(self, user_oid: str) -> UserModel | None:
        for user in self._saved_users:
            if user.oid == user_oid:
                return user

    async def get_by_username(self, user_oid: str) -> UserModel | None:
        for user in self._saved_users:
            if user.username == username:
                return user

    async def get_all(
        self, filters: GetUsersFilters
    ) -> tuple[Iterable[UserModel], int]:
        total_count = len(self._saved_users)
        limited_users = self._saved_users[
            filters.offset : filters.offset + filters.limit
        ]
        return limited_users, total_count

    async def delete(self, user_oid: str) -> UserModel | None:
        for user in self._saved_users:
            if user.oid == user_oid:
                self._saved_users.remove(user)
                return user

    async def check_user_exists_by_phone_and_username(
        self, phone: str, username: str
    ) -> bool:
        return any(
            user.phone.as_generic_type() == phone
            or user.username.as_generic_type() == username
            for user in self._saved_users
        )
