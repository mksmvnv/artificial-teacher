from typing import Any

import pytest

from src.schemas.user import UserSchema
from src.services import StartService


class TestStartService:
    """Test StartService."""

    USER_ID = 42

    @pytest.mark.asyncio
    async def test_register_new_user(
        self, start_service: StartService, mock_user_repository_protocol: Any, fake_user: UserSchema
    ) -> None:
        """Test registering new user."""
        # Arrange
        mock_user_repository_protocol.find_by_user_tg_id.return_value = None
        mock_user_repository_protocol.add_new_user.return_value = self.USER_ID

        # Act
        user_id = await start_service.register_user(fake_user)

        # Assert
        assert user_id == self.USER_ID
        mock_user_repository_protocol.find_by_user_tg_id.assert_called_once_with(fake_user.tg_id)
        mock_user_repository_protocol.add_new_user.assert_called_once_with(fake_user)

    @pytest.mark.asyncio
    async def test_register_existing_user(
        self, start_service: StartService, mock_user_repository_protocol: Any, fake_user: UserSchema
    ) -> None:
        """Test registering existing user."""
        # Arrange
        mock_user_repository_protocol.find_by_user_tg_id.return_value = fake_user

        # Act
        user_tg_id = await start_service.register_user(fake_user)

        # Assert
        assert user_tg_id == fake_user.tg_id
        mock_user_repository_protocol.find_by_user_tg_id.assert_called_once_with(fake_user.tg_id)
        mock_user_repository_protocol.add_new_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_register_user_without_optional_fields(
        self,
        start_service: StartService,
        mock_user_repository_protocol: Any,
        fake_user_without_optional: UserSchema,
    ) -> None:
        """Test registering user without optional fields."""
        # Arrange
        mock_user_repository_protocol.find_by_user_tg_id.return_value = None
        mock_user_repository_protocol.add_new_user.return_value = self.USER_ID

        # Act
        user_id = await start_service.register_user(fake_user_without_optional)

        # Assert
        assert user_id == self.USER_ID
        mock_user_repository_protocol.find_by_user_tg_id.assert_called_once_with(
            fake_user_without_optional.tg_id
        )
        mock_user_repository_protocol.add_new_user.assert_called_once_with(
            fake_user_without_optional
        )

    @pytest.mark.asyncio
    async def test_register_when_find_returns_user_without_optional_fields(
        self,
        start_service: StartService,
        mock_user_repository_protocol: Any,
        fake_user_without_optional: UserSchema,
    ) -> None:
        """Test registration when find returns user without optional fields."""
        # Arrange
        mock_user_repository_protocol.find_by_user_tg_id.return_value = fake_user_without_optional

        # Act
        user_tg_id = await start_service.register_user(fake_user_without_optional)

        # Assert
        assert user_tg_id == fake_user_without_optional.tg_id
        mock_user_repository_protocol.find_by_user_tg_id.assert_called_once_with(
            fake_user_without_optional.tg_id
        )
        mock_user_repository_protocol.add_new_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_service_initialization(self, mock_user_repository_protocol: Any) -> None:
        """Test that service initializes correctly."""
        # Act
        service = StartService(user_repository=mock_user_repository_protocol)

        # Assert
        assert service._user_repository == mock_user_repository_protocol
