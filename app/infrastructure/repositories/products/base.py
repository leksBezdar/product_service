from abc import ABC, abstractmethod
from typing import Iterable

from domain.entities.products import ProductEntity
from infrastructure.repositories.products.filters.products import GetProductsFilters


class IProductRepository(ABC):
    @abstractmethod
    async def add(self, product: ProductEntity) -> None: ...

    @abstractmethod
    async def get_by_oid(self, oid: str) -> ProductEntity | None: ...

    @abstractmethod
    async def get_by_title(self, title: str) -> ProductEntity | None: ...

    @abstractmethod
    async def get_all(
        self, filters: GetProductsFilters
    ) -> tuple[Iterable[ProductEntity], int]: ...

    @abstractmethod
    async def update(self, product: ProductEntity) -> ProductEntity: ...

    @abstractmethod
    async def delete(self, oid: str) -> ProductEntity | None: ...
