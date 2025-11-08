import logging

from src.repositories.user import UserRepositoryProtocol
from src.schemas.user import UserSchema

logger = logging.getLogger(__name__)


class StartService:
    """Start service."""

    def __init__(self, user_repository: UserRepositoryProtocol) -> None:
        self._user_repository = user_repository

    async def register_user(self, user: UserSchema) -> int:
        """Register user if not exists, return user id."""
        if existing_user := await self._user_repository.find_by_user_tg_id(user.tg_id):
            logger.info("User '%d' already exists", existing_user.tg_id)
            return existing_user.tg_id

        user_id = await self._user_repository.add_new_user(user)
        logger.info("User '%d' created with id '%d'", user.tg_id, user_id)
        return user_id
