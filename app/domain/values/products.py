from dataclasses import dataclass
import re

from domain.exceptions.products import (
    EmptyProductCategory,
    EmptyProductDescription,
    EmptyProductImage,
    EmptyProductPrice,
    EmptyProductQuantity,
    EmptyProductTag,
    EmptyProductTitle,
    EmptyProductVendor,
    EmptyProductWarrantyPeriod,
    EmptyStorageInstructions,
    InvalidProductCategoryLength,
    InvalidProductDescriptionLength,
    InvalidProductImage,
    InvalidProductPriceLength,
    InvalidProductQuantity,
    InvalidProductTagLength,
    InvalidProductTitleLength,
    InvalidProductVendorLength,
    InvalidStorageInstructionsLength,
    InvalidWarrantyPeriodLength,
)
from domain.values.base import BaseValueObject


@dataclass
class ProductTitle(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyProductTitle()

        value_length = len(self.value)

        if value_length not in range(3, 100):
            raise InvalidProductTitleLength(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class ProductDescription(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyProductDescription()

        value_length = len(self.value)

        if value_length not in range(10, 1000):
            raise InvalidProductDescriptionLength(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class ProductPrice(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyProductPrice()

        value_length = len(self.value)

        if value_length not in range(1, 10):
            raise InvalidProductPriceLength(self.value)


@dataclass
class ProductQuantity(BaseValueObject):
    value: int

    def validate(self) -> None:
        if not self.value:
            raise EmptyProductQuantity()

        if self.value < 0:
            raise InvalidProductQuantity()

    def as_generic_type(self) -> int:
        return self.value


@dataclass
class ProductVendor(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyProductVendor()

        value_length = len(self.value)

        if value_length not in range(3, 100):
            raise InvalidProductVendorLength(value_length)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class ProductImage(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyProductImage()

        if not re.match(r"^https?://[\w\.-]+(/\S*)?$", self.value):
            raise InvalidProductImage()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class ProductCategory(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyProductCategory()

        value_length = len(self.value)

        if value_length not in range(3, 100):
            raise InvalidProductCategoryLength(value_length)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class ProductTag(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyProductTag()

        value_length = len(self.value)

        if value_length not in range(3, 100):
            raise InvalidProductTagLength(value_length)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass
class ProductWarrantyPeriod(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyProductWarrantyPeriod()

        value_length = len(self.value)

        if value_length not in range(3, 20):
            raise InvalidWarrantyPeriodLength(value_length)


@dataclass
class ProductStorageInstructions(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyStorageInstructions()

        value_length = len(self.value)

        if value_length not in range(3, 1000):
            raise InvalidStorageInstructionsLength(value_length)
