from typing import Protocol

from src.models.user import User
from src.repositories.base import BaseRepository
from src.schemas.user import UserSchema


class UserRepositoryProtocol(Protocol):
    """Protocol for user repository."""

    async def find_by_tg_id(self, tg_id: int) -> UserSchema | None:
        """Find user by telegram id or none."""
        ...

    async def add_one(self, data: UserSchema) -> int:
        """Set user language by telegram id."""
        ...

    async def set_user_language(self, language: str, tg_id: int) -> None:
        """Set user language by telegram id."""
        ...

    async def get_user_language(self, tg_id: int) -> str | None:
        """Get user language by telegram id or none."""
        ...

    async def set_user_cefr_level(self, cefr_level: str, tg_id: int) -> None:
        """Set user language by telegram id."""
        ...

    async def get_user_cefr_level(self, tg_id: int) -> str | None:
        """Get user language by telegram id or none."""
        ...


class UserRepository(BaseRepository[User, UserSchema], UserRepositoryProtocol):
    """User repository."""

    model = User

    async def find_by_tg_id(self, tg_id: int) -> UserSchema | None:
        """Find user by telegram id or none."""
        user = await self.find_one_or_none(tg_id=tg_id)
        if user:
            return UserSchema(
                tg_id=user.tg_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
            )
        return None

    async def set_user_language(self, language: str, tg_id: int) -> None:
        """Set user language by telegram id."""
        await self.update_one(field_name="language", update_data=language, tg_id=tg_id)

    async def get_user_language(self, tg_id: int) -> str | None:
        """Get user language by telegram id or none."""
        user = await self.find_one_or_none(tg_id=tg_id)
        return user.language if user else None

    async def set_user_cefr_level(self, cefr_level: str, tg_id: int) -> None:
        """Set user language by telegram id."""
        await self.update_one(field_name="cefr_level", update_data=cefr_level, tg_id=tg_id)

    async def get_user_cefr_level(self, tg_id: int) -> str | None:
        """Get user language by telegram id or none."""
        user = await self.find_one_or_none(tg_id=tg_id)
        return user.cefr_level if user else None
