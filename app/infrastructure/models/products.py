from datetime import datetime
from typing import Any, ClassVar

from sqlalchemy import ARRAY, TIMESTAMP, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from infrastructure.models.common.base import Base, BaseIDMixin


class ProductModel(Base, BaseIDMixin):
    __mapper_args__: ClassVar[dict[Any, Any]] = {"eager_defaults": True}

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    vendor: Mapped[str] = mapped_column(nullable=False)

    images: Mapped[list] = mapped_column(ARRAY(String), nullable=False, default=[])
    categories: Mapped[list] = mapped_column(ARRAY(String), nullable=False, default=[])
    tags: Mapped[list] = mapped_column(ARRAY(String), nullable=False, default=[])
    warranty_period: Mapped[str | None] = mapped_column(default=None)
    storage_instructions: Mapped[list] = mapped_column(
        ARRAY(String), nullable=False, default=[]
    )

    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), default=None
    )

    def __str__(self):
        return self.title
