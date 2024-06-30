from dataclasses import dataclass

from infrastructure.repositories.common.filters.base import BaseGetAllFilters


@dataclass
class GetProductsFilters(BaseGetAllFilters):
    limit: int = 10
    offset: int = 0
