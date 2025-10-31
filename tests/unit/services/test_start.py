from unittest.mock import AsyncMock

import pytest

from src.schemas.user import UserSchema
from src.services.start import StartService


class TestStartService:
    """Test StartService."""

    @pytest.mark.asyncio
    async def test_register_new_user(
        self, mock_user_repository: AsyncMock, fake_user: UserSchema
    ) -> None:
        """Test registering new user."""
        mock_user_repository.find_by_tg_id.return_value = None
        mock_user_repository.add_one.return_value = 42

        service = StartService(mock_user_repository)
        user_id = await service.register_user(fake_user)

        assert user_id == 42

        mock_user_repository.find_by_tg_id.assert_called_once_with(123456789)
        mock_user_repository.add_one.assert_called_once_with(fake_user)

    @pytest.mark.asyncio
    async def test_register_existing_user(
        self, mock_user_repository: AsyncMock, fake_user: UserSchema
    ) -> None:
        """Test registering existing user."""
        mock_user_repository.find_by_tg_id.return_value = fake_user

        service = StartService(mock_user_repository)
        user_id = await service.register_user(fake_user)

        assert user_id == 123456789

        mock_user_repository.find_by_tg_id.assert_called_once_with(123456789)
        mock_user_repository.add_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_register_user_without_optional_fields(
        self, mock_user_repository: AsyncMock, fake_user_without_optional: UserSchema
    ) -> None:
        """Test registering user without optional fields."""
        mock_user_repository.find_by_tg_id.return_value = None
        mock_user_repository.add_one.return_value = 42

        service = StartService(mock_user_repository)
        user_id = await service.register_user(fake_user_without_optional)

        assert user_id == 42
        mock_user_repository.find_by_tg_id.assert_called_once_with(123456790)
        mock_user_repository.add_one.assert_called_once_with(fake_user_without_optional)

    @pytest.mark.asyncio
    async def test_register_when_find_returns_none(
        self, mock_user_repository: AsyncMock, fake_user_without_optional: UserSchema
    ) -> None:
        """Test registration when find returns user without optional fields."""
        mock_user_repository.find_by_tg_id.return_value = fake_user_without_optional

        service = StartService(mock_user_repository)
        user_id = await service.register_user(fake_user_without_optional)

        assert user_id == 123456790
        mock_user_repository.add_one.assert_not_called()
