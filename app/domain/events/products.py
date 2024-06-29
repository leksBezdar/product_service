from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class ProductCreatedEvent(BaseEvent):
    title: ClassVar[str] = "Product Created"

    product_oid: str
    title: str
    vendor: str


@dataclass
class ProductChangedTitleEvent(BaseEvent):
    title: ClassVar[str] = "Product Title Changed"

    product_oid: str


@dataclass
class ProductChangedDescriptionEvent(BaseEvent):
    title: ClassVar[str] = "Product Description Changed"

    product_oid: str


@dataclass
class ProductChangedPriceEvent(BaseEvent):
    title: ClassVar[str] = "Product Price Changed"

    product_oid: str


@dataclass
class ProductChangedQuantityEvent(BaseEvent):
    title: ClassVar[str] = "Product Quantity Changed"

    product_oid: str


@dataclass
class ProductChangedVendorEvent(BaseEvent):
    title: ClassVar[str] = "Product Vendor Changed"

    product_oid: str


@dataclass
class ProductUpdatedImagesEvent(BaseEvent):
    title: ClassVar[str] = "Product Images Updated"

    product_oid: str


@dataclass
class ProductUpdatedCategoriesEvent(BaseEvent):
    title: ClassVar[str] = "Product Categories Updated"

    product_oid: str


@dataclass
class ProductUpdatedTagsEvent(BaseEvent):
    title: ClassVar[str] = "Product Tags Updated"

    product_oid: str


@dataclass
class ProductUpdatedWarrantyPeriodEvent(BaseEvent):
    title: ClassVar[str] = "Product Warranty Period Updated"

    product_oid: str


@dataclass
class ProductUpdatedStorageInstructionsEvent(BaseEvent):
    title: ClassVar[str] = "Product Storage Instructions Updated"

    product_oid: str


@dataclass
class ProductDeletedEvent(BaseEvent):
    title: ClassVar[str] = "Product Deleted"

    product_oid: str
    title: str
    vendor: str
