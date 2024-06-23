from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.groups import UserGroup
from domain.entities.users import User
from infrastructure.repositories.groups.base import (
    BaseGroupRepository,
)
from infrastructure.repositories.groups.filters.groups import (
    GetGroupsFilters,
)
from logic.exceptions.groups import GroupNotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetGroupQuery(BaseQuery):
    group_oid: str


@dataclass(frozen=True)
class GetGroupsQuery(BaseQuery):
    filters: GetGroupsFilters


@dataclass(frozen=True)
class GetGroupQueryHandler(BaseQueryHandler):
    group_repository: BaseGroupRepository

    async def handle(self, query: GetGroupQuery) -> UserGroup:
        group = await self.group_repository.get_group_by_oid(group_oid=query.group_oid)

        if not group:
            raise GroupNotFoundException(oid=query.group_oid)

        return group


@dataclass(frozen=True)
class GetGroupsQueryHandler(BaseQueryHandler):
    groups_repository: BaseGroupRepository

    async def handle(self, query: GetGroupsQuery) -> Iterable[User]:
        return await self.groups_repository.get_groups(filters=query.filters)
