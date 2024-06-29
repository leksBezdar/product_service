from dataclasses import dataclass
from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class EmptyProductTitle(ApplicationException):
    @property
    def message(self) -> str:
        return "Product title is empty"


@dataclass(eq=False)
class InvalidProductTitleLength(ApplicationException):
    title_value: str

    @property
    def message(self) -> str:
        return f"Product title length is invalid: {self.title_value}"


@dataclass(eq=False)
class EmptyProductDescription(ApplicationException):
    @property
    def message(self) -> str:
        return "Product description is empty"


@dataclass(eq=False)
class InvalidProductDescriptionLength(ApplicationException):
    description_value: str

    @property
    def message(self) -> str:
        return f"Product description length is invalid: {self.description_value}"


@dataclass(eq=False)
class EmptyProductPrice(ApplicationException):
    @property
    def message(self) -> str:
        return "Product price is empty"


@dataclass(eq=False)
class InvalidProductPriceLength(ApplicationException):
    price_value: str

    @property
    def message(self) -> str:
        return f"Product price length is invalid: {self.price_value}"


@dataclass(eq=False)
class EmptyProductQuantity(ApplicationException):
    @property
    def message(self) -> str:
        return "Product quantity is empty"


@dataclass(eq=False)
class InvalidProductQuantity(ApplicationException):
    @property
    def message(self) -> str:
        return "Product quantity is invalid, it must be a non-negative integer"


@dataclass(eq=False)
class EmptyProductVendor(ApplicationException):
    @property
    def message(self) -> str:
        return "Product vendor is empty"


@dataclass(eq=False)
class InvalidProductVendorLength(ApplicationException):
    vendor_length: int

    @property
    def message(self) -> str:
        return f"Product vendor length is invalid: {self.vendor_length}"


@dataclass(eq=False)
class EmptyProductImage(ApplicationException):
    @property
    def message(self) -> str:
        return "Product image URL is empty"


@dataclass(eq=False)
class InvalidProductImage(ApplicationException):
    image_url: str

    @property
    def message(self) -> str:
        return f"The provided product image URL is invalid: {self.image_url}"


@dataclass(eq=False)
class EmptyProductCategory(ApplicationException):
    @property
    def message(self) -> str:
        return "Product category is empty"


@dataclass(eq=False)
class InvalidProductCategoryLength(ApplicationException):
    category_length: int

    @property
    def message(self) -> str:
        return f"Product category length is invalid: {self.category_length}"


@dataclass(eq=False)
class EmptyProductTag(ApplicationException):
    @property
    def message(self) -> str:
        return "Product tag is empty"


@dataclass(eq=False)
class InvalidProductTagLength(ApplicationException):
    tag_length: int

    @property
    def message(self) -> str:
        return f"Product tag length is invalid: {self.tag_length}"


@dataclass(eq=False)
class EmptyProductWarrantyPeriod(ApplicationException):
    @property
    def message(self) -> str:
        return "Product warranty period is empty"


@dataclass(eq=False)
class InvalidWarrantyPeriodLength(ApplicationException):
    warranty_length: int

    @property
    def message(self) -> str:
        return f"Product warranty period length is invalid: {self.warranty_length}"


@dataclass(eq=False)
class EmptyStorageInstructions(ApplicationException):
    @property
    def message(self) -> str:
        return "Product storage instructions are empty"


@dataclass(eq=False)
class InvalidStorageInstructionsLength(ApplicationException):
    instructions_length: int

    @property
    def message(self) -> str:
        return f"Product storage instructions length is invalid: {self.instructions_length}"


@dataclass(eq=False)
class ProductAlreadyDeleted(ApplicationException):
    value: str

    @property
    def message(self) -> str:
        return f"Product with id {self.value} has already been deleted"
