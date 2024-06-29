from dataclasses import field, dataclass
from datetime import UTC, datetime

from domain.entities.base import BaseEntity
from domain.events.products import (
    ProductChangedDescriptionEvent,
    ProductChangedPriceEvent,
    ProductChangedQuantityEvent,
    ProductChangedTitleEvent,
    ProductChangedVendorEvent,
    ProductCreatedEvent,
    ProductDeletedEvent,
    ProductUpdatedCategoriesEvent,
    ProductUpdatedImagesEvent,
    ProductUpdatedStorageInstructionsEvent,
    ProductUpdatedTagsEvent,
    ProductUpdatedWarrantyPeriodEvent,
)
from domain.exceptions.products import ProductAlreadyDeleted
from domain.values.products import (
    ProductCategory,
    ProductDescription,
    ProductImage,
    ProductPrice,
    ProductQuantity,
    ProductStorageInstructions,
    ProductTag,
    ProductTitle,
    ProductVendor,
    ProductWarrantyPeriod,
)


@dataclass(eq=False)
class ProductEntity(BaseEntity):
    title: ProductTitle
    description: ProductDescription
    price: ProductPrice
    quantity: ProductQuantity
    images: list[ProductImage] = field(default_factory=list)
    categories: list[ProductCategory] = field(default_factory=list)
    tags: list[ProductTag] = field(default_factory=list)
    warranty_period: ProductWarrantyPeriod | None = field(default=None)
    storage_instructions: list[ProductStorageInstructions] = field(default_factory=list)
    vendor: ProductVendor

    is_deleted: bool = field(default=False, kw_only=True)

    created_at: datetime = field(default_factory=datetime.now(UTC), kw_only=True)
    updated_at: datetime = field(default_factory=datetime.now(UTC), kw_only=True)
    deleted_at: datetime | None = field(default=None, kw_only=True)

    @classmethod
    async def create(
        cls,
        title: ProductTitle,
        description: ProductDescription,
        price: ProductPrice,
        quantity: ProductQuantity,
        vendor: ProductVendor,
        images: list[ProductImage] = [],
        categories: list[ProductCategory] = [],
        tags: list[ProductTag] = [],
        warranty_period: ProductWarrantyPeriod | None = None,
        storage_instructions: list[ProductStorageInstructions] = [],
    ) -> "ProductEntity":
        new_product = cls(
            title=title,
            description=description,
            price=price,
            quantity=quantity,
            vendor=vendor,
            images=images,
            categories=categories,
            tags=tags,
            warranty_period=warranty_period,
            storage_instructions=storage_instructions,
        )
        new_product.register_event(
            ProductCreatedEvent(
                product_oid=new_product.oid,
                title=new_product.title.as_generic_type(),
                vendor=new_product.vendor.as_generic_type(),
            )
        )
        return new_product

    async def change_title(self, new_title: ProductTitle) -> None:
        self._validate_not_deleted()
        self.title = new_title

        self.register_event(
            ProductChangedTitleEvent(
                product_oid=self.oid,
            )
        )

    async def change_description(self, new_description: ProductDescription) -> None:
        self._validate_not_deleted()
        self.description = new_description

        self.register_event(
            ProductChangedDescriptionEvent(
                product_oid=self.oid,
            )
        )

    async def change_price(self, new_price: ProductPrice) -> None:
        self._validate_not_deleted()
        self.price = new_price

        self.register_event(
            ProductChangedPriceEvent(
                product_oid=self.oid,
            )
        )

    async def change_quantity(self, new_quantity: ProductQuantity) -> None:
        self._validate_not_deleted()
        self.quantity = new_quantity

        self.register_event(
            ProductChangedQuantityEvent(
                product_oid=self.oid,
            )
        )

    async def change_vendor(self, new_vendor: ProductVendor) -> None:
        self._validate_not_deleted()
        self.vendor = new_vendor

        self.register_event(
            ProductChangedVendorEvent(
                product_oid=self.oid,
            )
        )

    async def update_images(self, new_images: list[ProductImage]) -> None:
        self._validate_not_deleted()
        self.images = new_images

        self.register_event(
            ProductUpdatedImagesEvent(
                product_oid=self.oid,
            )
        )

    async def update_categories(self, new_categories: list[ProductCategory]) -> None:
        self._validate_not_deleted()
        self.categories = new_categories

        self.register_event(
            ProductUpdatedCategoriesEvent(
                product_oid=self.oid,
            )
        )

    async def update_tags(self, new_tags: list[ProductTag]) -> None:
        self._validate_not_deleted()
        self.tags = new_tags

        self.register_event(
            ProductUpdatedTagsEvent(
                product_oid=self.oid,
            )
        )

    async def update_warranty_period(
        self, new_warranty_period: ProductWarrantyPeriod
    ) -> None:
        self._validate_not_deleted()
        self.warranty_period = new_warranty_period

        self.register_event(
            ProductUpdatedWarrantyPeriodEvent(
                product_oid=self.oid,
            )
        )

    async def update_storage_instructions(
        self, new_storage_instructions: list[ProductStorageInstructions]
    ) -> None:
        self._validate_not_deleted()
        self.storage_instructions = new_storage_instructions

        self.register_event(
            ProductUpdatedStorageInstructionsEvent(
                product_oid=self.oid,
            )
        )

    def delete(self) -> None:
        self._validate_not_deleted()
        self.deleted_at = datetime.now(UTC)

        self.register_event(
            ProductDeletedEvent(
                product_oid=self.oid,
                title=self.title.as_generic_type(),
                vendor=self.vendor.as_generic_type(),
            )
        )

    def _validate_not_deleted(self) -> None:
        if self.deleted_at is not None:
            raise ProductAlreadyDeleted(self.oid)
