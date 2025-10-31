from src.models.user import User
from src.repositories.base import BaseRepository
from src.schemas.user import UserSchema


class UserRepository(BaseRepository[User, UserSchema]):
    """User repository."""

    model = User

    async def find_by_tg_id(self, tg_id: int) -> User | None:
        """Find user by telegram id or none."""
        return await self.find_one_or_none(tg_id=tg_id)

    async def set_user_language(self, language: str, tg_id: int) -> None:
        """Set user language by telegram id."""
        await self.update_one(field_name="language", update_data=language, tg_id=tg_id)

    async def get_user_language(self, tg_id: int) -> str | None:
        """Get user language by telegram id or none."""
        user = await self.find_by_tg_id(tg_id)
        return user.language if user else None

    async def set_user_cefr_level(self, cefr_level: str, tg_id: int) -> None:
        """Set user language by telegram id."""
        await self.update_one(field_name="cefr_level", update_data=cefr_level, tg_id=tg_id)

    async def get_user_cefr_level(self, tg_id: int) -> str | None:
        """Get user language by telegram id or none."""
        user = await self.find_by_tg_id(tg_id)
        return user.cefr_level if user else None
