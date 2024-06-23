from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.users import User
from infrastructure.repositories.users.base import (
    BaseUserRepository,
)
from infrastructure.repositories.users.filters.users import (
    GetUsersFilters,
)
from infrastructure.security.cookies.base import BaseCookieManager
from logic.exceptions.users import UserNotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass
class Tokens:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class GetTokensQuery(BaseQuery):
    username: str


@dataclass(frozen=True)
class GetUsersQuery(BaseQuery):
    group_oid: str
    filters: GetUsersFilters


@dataclass(frozen=True)
class GetUserQuery(BaseQuery):
    user_oid: str


@dataclass(frozen=True)
class GetTokensQueryHandler(BaseQueryHandler):
    cookie_manager: BaseCookieManager
    user_repository: BaseUserRepository

    async def handle(self, query: GetTokensQuery) -> Tokens:
        user = await self.user_repository.get_user_by_username(query.username)
        if not user:
            raise UserNotFoundException(query.username)

        access_token = await self.cookie_manager.create_access_token(user.oid)
        refresh_token = await self.cookie_manager.create_refresh_token(user.oid)

        return Tokens(access_token=access_token, refresh_token=refresh_token)


@dataclass(frozen=True)
class GetUserQueryHandler(BaseQueryHandler):
    user_repository: BaseUserRepository

    async def handle(self, query: GetUserQuery) -> User:
        user = await self.user_repository.get_user_by_oid(user_oid=query.user_oid)
        if not user:
            raise UserNotFoundException(value=query.user_oid)

        return user


@dataclass(frozen=True)
class GetUsersQueryHandler(BaseQueryHandler):
    user_repository: BaseUserRepository

    async def handle(self, query: GetUsersQuery) -> Iterable[User]:
        return await self.user_repository.get_users(
            group_oid=query.group_oid, filters=query.filters
        )
