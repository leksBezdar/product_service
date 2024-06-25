from abc import ABC, abstractmethod
from typing import Iterable

from infrastructure.models.users import UserModel
from infrastructure.repositories.users.filters.users import GetUsersFilters


class IUserRepository(ABC):
    @abstractmethod
    async def add(self, user: UserModel) -> None: ...

    @abstractmethod
    async def get_by_oid(self, oid: str) -> UserModel | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> UserModel | None: ...

    @abstractmethod
    async def get_all(
        self, filters: GetUsersFilters
    ) -> tuple[Iterable[UserModel], int]: ...

    @abstractmethod
    async def delete(self, oid: str) -> UserModel | None: ...

    @abstractmethod
    async def check_user_exists_by_phone_and_username(
        self, phone: str, username: str
    ) -> bool: ...
