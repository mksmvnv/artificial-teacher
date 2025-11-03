import logging

from redis.asyncio import Redis as redis

from src.core.config import settings

logger = logging.getLogger(__name__)


class ContextService:
    """Redis context service."""

    def __init__(self) -> None:
        self._url = settings.context.url
        self._ttl = settings.context.ttl
        self._client = redis.from_url(
            url=self._url,
            decode_responses=True,
        )

    async def set_user_language(self, tg_id: int, language: str) -> None:
        """Set user language in redis context."""
        key = f"user_language:{tg_id}"
        await self._client.setex(name=key, time=self._ttl, value=language)
        logger.info("Set language '%s' for user '%d'", language, tg_id)

    async def get_user_language(self, tg_id: int) -> str | None:
        """Get user language from redis context."""
        key = f"user_language:{tg_id}"
        data: str | None = await self._client.get(key)
        logger.info("Received language '%s' for user '%d'", data, tg_id)
        return data
