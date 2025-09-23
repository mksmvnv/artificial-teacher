from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class Base(AsyncAttrs, DeclarativeBase):
    """Base model."""

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        """Prepare table name."""
        return cls.__name__.lower() + "s"
