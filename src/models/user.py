from typing import Final

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base

USERNAME_MAX_LENGTH: Final[int] = 32
FIRST_NAME_MAX_LENGTH: Final[int] = 64
LAST_NAME_MAX_LENGTH: Final[int] = 64


class User(Base):
    """Telegram user model."""

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(USERNAME_MAX_LENGTH), index=True)
    first_name: Mapped[str] = mapped_column(String(FIRST_NAME_MAX_LENGTH))
    last_name: Mapped[str] = mapped_column(String(LAST_NAME_MAX_LENGTH))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
