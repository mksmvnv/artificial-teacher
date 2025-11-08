import logging

from src.repositories.user import UserRepositoryProtocol

logger = logging.getLogger(__name__)


class LanguageService:
    """Language parameters service."""

    def __init__(self, user_repository: UserRepositoryProtocol) -> None:
        self._user_repository = user_repository

    async def set_user_language(self, user_tg_id: int, language: str) -> None:
        """Set user language."""
        user = await self._user_repository.find_by_user_tg_id(user_tg_id)

        if user is None:
            logger.warning("User '%d' not found in database", user_tg_id)
            return None

        current_language = await self._user_repository.get_user_language(user_tg_id=user_tg_id)

        # If the language is the same, do nothing
        if current_language == language:
            logger.info("User '%d' selected the same language '%s'", user_tg_id, language)
            return None

        await self._user_repository.set_user_language(language=language, user_tg_id=user_tg_id)
        logger.info("User '%d' language set to '%s'", user_tg_id, language)

    async def get_user_language(self, user_tg_id: int) -> str | None:
        """Get user language."""
        user = await self._user_repository.find_by_user_tg_id(user_tg_id)

        if user is None:
            logger.warning("User '%d' not found in database", user_tg_id)
            return None

        language = await self._user_repository.get_user_language(user_tg_id=user_tg_id)

        if language is None:
            logger.warning("User '%d' language not found in database", user_tg_id)
            return None

        logger.info("User '%d' language is '%s'", user_tg_id, language)
        return language

    async def set_user_cefr_level(self, user_tg_id: int, cefr_level: str) -> None:
        """Set user CEFR level."""
        user = await self._user_repository.find_by_user_tg_id(user_tg_id)

        if user is None:
            logger.warning("User '%d' not found in database", user_tg_id)
            return None

        current_cefr_level = await self._user_repository.get_user_cefr_level(user_tg_id=user_tg_id)

        # If the CEFR level is the same, do nothing
        if current_cefr_level == cefr_level:
            logger.info("User '%d' selected the same CEFR level %s", user_tg_id, cefr_level)
            return None

        await self._user_repository.set_user_cefr_level(
            cefr_level=cefr_level, user_tg_id=user_tg_id
        )
        logger.info("User '%d' CEFR level set to '%s'", user_tg_id, cefr_level)

    async def get_user_cefr_level(self, user_tg_id: int) -> str | None:
        """Get user CEFR level."""
        user = await self._user_repository.find_by_user_tg_id(user_tg_id)

        if user is None:
            logger.warning("User '%d' not found in database", user_tg_id)
            return None

        cefr_level = await self._user_repository.get_user_cefr_level(user_tg_id=user_tg_id)

        if cefr_level is None:
            logger.warning("User '%d' CEFR level not found in database", user_tg_id)
            return None

        logger.info("User '%d' CEFR level is '%s'", user_tg_id, cefr_level)
        return cefr_level
