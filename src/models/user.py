from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class User(Base):
    """User model."""

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(length=32), nullable=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(length=64), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(length=64), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    language: Mapped[str | None] = mapped_column(String(length=10), nullable=True)
    cefr_level: Mapped[str | None] = mapped_column(String(length=2), nullable=True)
