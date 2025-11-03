from unittest.mock import AsyncMock, patch

import pytest

from src.services import ContextService


@pytest.fixture
def context_service() -> ContextService:
    """Create ContextService with mocked redis."""
    with patch("src.services.context.redis") as mock_redis_class:
        mock_client = AsyncMock()
        mock_redis_class.from_url.return_value = mock_client
        service = ContextService()
        service._client = mock_client
        return service


class TestContextService:
    """Test ContextService class."""

    USER_TG_ID = 123456789
    EN_LANG = "EN"
    REDIS_URL = "redis://localhost:6379"
    REDIS_TTL = 3600

    @pytest.mark.asyncio
    async def test_set_user_language_success(self, context_service: ContextService) -> None:
        """Test successful language setting."""
        # Arrange
        context_service._client.setex = AsyncMock()

        # Act
        await context_service.set_user_language(self.USER_TG_ID, self.EN_LANG)

        # Assert
        expected_key = f"user_language:{self.USER_TG_ID}"
        context_service._client.setex.assert_called_once_with(
            name=expected_key, time=context_service._ttl, value=self.EN_LANG
        )

    @pytest.mark.asyncio
    async def test_get_user_language_success(self, context_service: ContextService) -> None:
        """Test successful language retrieval."""
        # Arrange
        context_service._client.get = AsyncMock(return_value=self.EN_LANG)

        # Act
        result = await context_service.get_user_language(self.USER_TG_ID)

        # Assert
        expected_key = f"user_language:{self.USER_TG_ID}"
        context_service._client.get.assert_called_once_with(expected_key)
        assert result == self.EN_LANG

    @pytest.mark.asyncio
    async def test_get_user_language_not_found(self, context_service: ContextService) -> None:
        """Test language retrieval when not found."""
        # Arrange
        context_service._client.get = AsyncMock(return_value=None)

        # Act
        result = await context_service.get_user_language(self.USER_TG_ID)

        # Assert
        expected_key = f"user_language:{self.USER_TG_ID}"
        context_service._client.get.assert_called_once_with(expected_key)
        assert result is None

    @pytest.mark.asyncio
    async def test_service_initialization(self) -> None:
        """Test service initialization with settings."""
        with (
            patch("src.services.context.settings") as mock_settings,
            patch("src.services.context.redis") as mock_redis_class,
        ):
            # Arrange
            mock_settings.context.url = self.REDIS_URL
            mock_settings.context.ttl = self.REDIS_TTL
            mock_client = AsyncMock()
            mock_redis_class.from_url.return_value = mock_client

            # Act
            service = ContextService()

            # Assert
            assert service._url == self.REDIS_URL
            assert service._ttl == self.REDIS_TTL
            mock_redis_class.from_url.assert_called_once_with(
                url=self.REDIS_URL, decode_responses=True
            )
