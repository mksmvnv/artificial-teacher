from src.models.user import User
from src.repositories.base import BaseRepository
from src.schemas.user import UserSchema


class UserRepository(BaseRepository[User, UserSchema]):
    """User repository."""

    model = User

    async def find_by_tg_id(self, tg_id: int) -> User | None:
        """Find user by telegram id or none."""
        return await self.find_one_or_none(tg_id=tg_id)
