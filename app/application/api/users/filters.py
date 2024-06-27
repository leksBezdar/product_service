from dataclasses import dataclass

from application.api.common.filters.base import BaseGetAllFilters
from infrastructure.repositories.users.filters.users import (
    GetUsersFilters as GetUsersInfrastructureFilters,
)


@dataclass
class GetUsersFilters(BaseGetAllFilters):
    limit: int = 10
    offset: int = 0

    def to_infrastructure_filters(self):
        return GetUsersInfrastructureFilters(limit=self.limit, offset=self.offset)
