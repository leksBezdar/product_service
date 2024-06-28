from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.users import UserEntity
from infrastructure.repositories.users.base import (
    IUserRepository,
)
from infrastructure.repositories.users.filters.users import (
    GetUsersFilters,
)
from logic.exceptions.users import UserNotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetUsersQuery(BaseQuery):
    filters: GetUsersFilters


@dataclass(frozen=True)
class GetUserQuery(BaseQuery):
    user_oid: str


@dataclass(frozen=True)
class GetUserQueryHandler(BaseQueryHandler):
    user_repository: IUserRepository

    async def handle(self, query: GetUserQuery) -> UserEntity:
        user = await self.user_repository.get_by_oid(oid=query.user_oid)
        if not user:
            raise UserNotFoundException(value=query.user_oid)

        return user


@dataclass(frozen=True)
class GetUsersQueryHandler(BaseQueryHandler):
    user_repository: IUserRepository

    async def handle(self, query: GetUsersQuery) -> Iterable[UserEntity]:
        return await self.user_repository.get_all(filters=query.filters)
