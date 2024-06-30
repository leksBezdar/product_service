from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class ProductCreatedEvent(BaseEvent):
    title: ClassVar[str] = "Product Created"

    product_oid: str
    title: str
    vendor: str
    description: str
    price: float
    quantity: int
    images: list[str]
    categories: list[str]
    tags: list[str]
    warranty_period: str | None
    storage_instructions: list[str]


@dataclass
class ProductChangedTitleEvent(BaseEvent):
    title: ClassVar[str] = "Product Title Changed"

    product_oid: str
    old_title: str
    new_title: str


@dataclass
class ProductChangedDescriptionEvent(BaseEvent):
    title: ClassVar[str] = "Product Description Changed"

    product_oid: str
    old_description: str
    new_description: str


@dataclass
class ProductChangedPriceEvent(BaseEvent):
    title: ClassVar[str] = "Product Price Changed"

    product_oid: str
    old_price: float
    new_price: float


@dataclass
class ProductChangedQuantityEvent(BaseEvent):
    title: ClassVar[str] = "Product Quantity Changed"

    product_oid: str
    old_quantity: int
    new_quantity: int


@dataclass
class ProductChangedVendorEvent(BaseEvent):
    title: ClassVar[str] = "Product Vendor Changed"

    product_oid: str
    old_vendor: str
    new_vendor: str


@dataclass
class ProductUpdatedImagesEvent(BaseEvent):
    title: ClassVar[str] = "Product Images Updated"

    product_oid: str
    old_images: list[str]
    new_images: list[str]


@dataclass
class ProductUpdatedCategoriesEvent(BaseEvent):
    title: ClassVar[str] = "Product Categories Updated"

    product_oid: str
    old_categories: list[str]
    new_categories: list[str]


@dataclass
class ProductUpdatedTagsEvent(BaseEvent):
    title: ClassVar[str] = "Product Tags Updated"

    product_oid: str
    old_tags: list[str]
    new_tags: list[str]


@dataclass
class ProductUpdatedWarrantyPeriodEvent(BaseEvent):
    title: ClassVar[str] = "Product Warranty Period Updated"

    product_oid: str
    old_warranty_period: str | None
    new_warranty_period: str | None


@dataclass
class ProductUpdatedStorageInstructionsEvent(BaseEvent):
    title: ClassVar[str] = "Product Storage Instructions Updated"

    product_oid: str
    old_storage_instructions: list[str]
    new_storage_instructions: list[str]


@dataclass
class ProductDeletedEvent(BaseEvent):
    title: ClassVar[str] = "Product Deleted"

    product_oid: str
    title: str
    vendor: str
