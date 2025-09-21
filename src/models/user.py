from enum import IntEnum

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class StringLength(IntEnum):
    USERNAME = 32
    FIRST_NAME = 64
    LAST_NAME = 64


class User(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(StringLength.USERNAME), index=True)
    first_name: Mapped[str] = mapped_column(String(StringLength.FIRST_NAME))
    last_name: Mapped[str] = mapped_column(String(StringLength.LAST_NAME))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
