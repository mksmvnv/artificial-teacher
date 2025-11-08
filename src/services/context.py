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

    async def set_context(self, prefix: str, user_tg_id: int, data: str) -> None:
        """Set data in redis context."""
        key = f"{prefix}:{user_tg_id}"
        await self._client.setex(name=key, time=self._ttl, value=data)
        logger.info("Set context '%s' with data '%s' for user '%d'", prefix, data, user_tg_id)

    async def get_context(self, prefix: str, user_tg_id: int) -> str | None:
        """Get data from redis context."""
        key = f"{prefix}:{user_tg_id}"
        data: str | None = await self._client.get(key)

        if data is None:
            logger.info("Context '%s' not found for user '%d'", prefix, user_tg_id)
            return None

        logger.info("Received context '%s' with data '%s' for user '%d'", prefix, data, user_tg_id)
        return data
