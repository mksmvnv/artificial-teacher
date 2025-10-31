import logging

from src.repositories.user import UserRepository

logger = logging.getLogger(__name__)


class LanguageService:
    """Language parameters service."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def set_user_language(self, tg_id: int, language: str) -> None:
        """Set user language."""
        existing = await self._user_repository.find_by_tg_id(tg_id)

        if not existing:
            logger.warning("User %d not found in database", tg_id)
            return None

        current_language = await self._user_repository.get_user_language(tg_id=tg_id)

        # If the language is the same, do nothing
        if current_language == language:
            logger.info("User %d selected the same language %s", tg_id, language)
            return None

        await self._user_repository.set_user_language(language=language, tg_id=tg_id)
        logger.info("User %d language set to %s", tg_id, language)

    async def get_user_language(self, tg_id: int) -> str | None:
        """Get user language."""
        existing = await self._user_repository.find_by_tg_id(tg_id)

        if not existing:
            logger.warning("User %d not found in database", tg_id)
            return None

        language = await self._user_repository.get_user_language(tg_id=tg_id)
        logger.info("User %d language is %s", tg_id, language)
        return language

    async def set_user_cefr_level(self, tg_id: int, cefr_level: str) -> None:
        """Set user CEFR level."""
        existing = await self._user_repository.find_by_tg_id(tg_id)

        if not existing:
            logger.warning("User %d not found in database", tg_id)
            return None

        current_cefr_level = await self._user_repository.get_user_cefr_level(tg_id=tg_id)

        # If the CEFR level is the same, do nothing
        if current_cefr_level == cefr_level:
            logger.info("User %d selected the same CEFR level %s", tg_id, cefr_level)
            return None

        await self._user_repository.set_user_cefr_level(cefr_level=cefr_level, tg_id=tg_id)
        logger.info("User %d CEFR level set to %s", tg_id, cefr_level)
