from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import select, update
from sqlalchemy.engine import Result

from src.models.user import User
from src.repositories.base import BaseRepository
from src.schemas.user import UserSchema


class TestBaseRepository:
    """Test BaseRepository class."""

    USER_ID = 1
    NONEXISTENT_USER_TG_ID = 987654321
    EN_LANG = "EN"

    @pytest.mark.asyncio
    async def test_find_one_or_none_found(
        self, mock_session_factory: Any, mock_async_session: Any, user_model: User
    ) -> None:
        """Test finding one object when exists."""
        # Arrange
        repo = BaseRepository[User, UserSchema](mock_session_factory)
        repo.model = User

        mock_result = MagicMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = user_model
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.find_one_or_none(tg_id=user_model.tg_id)

        # Assert
        assert result == user_model
        mock_async_session.execute.assert_called_once()
        call_args = mock_async_session.execute.call_args[0][0]
        assert str(call_args) == str(select(User).filter_by(tg_id=user_model.tg_id))

    @pytest.mark.asyncio
    async def test_find_one_or_none_not_found(
        self, mock_session_factory: Any, mock_async_session: Any
    ) -> None:
        """Test finding one object when not exists."""
        # Arrange
        repo = BaseRepository[User, UserSchema](mock_session_factory)
        repo.model = User

        mock_result = MagicMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await repo.find_one_or_none(tg_id=self.NONEXISTENT_USER_TG_ID)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_add_one_success(
        self,
        mock_session_factory: Any,
        mock_async_session: Any,
        fake_user: UserSchema,
    ) -> None:
        """Test adding one object."""
        # Arrange
        repo = BaseRepository[User, UserSchema](mock_session_factory)
        repo.model = User

        with (
            patch.object(repo.model, "__init__", lambda self, **kwargs: None),
            patch.object(repo.model, "id", self.USER_ID),
        ):
            # Act
            result = await repo.add_one(fake_user)

        # Assert
        assert result == 1
        mock_async_session.add.assert_called_once()
        mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_one_success(
        self, mock_session_factory: Any, mock_async_session: Any
    ) -> None:
        """Test updating one object."""
        # Arrange
        repo = BaseRepository[User, UserSchema](mock_session_factory)
        repo.model = User

        mock_result = MagicMock(spec=Result)
        mock_async_session.execute.return_value = mock_result

        # Act
        await repo.update_one("language", self.EN_LANG, tg_id=self.NONEXISTENT_USER_TG_ID)

        # Assert
        mock_async_session.execute.assert_called_once()
        call_args = mock_async_session.execute.call_args[0][0]
        expected_query = (
            update(User).filter_by(tg_id=self.NONEXISTENT_USER_TG_ID).values(language=self.EN_LANG)
        )
        assert str(call_args) == str(expected_query)
        mock_async_session.commit.assert_called_once()

    def test_get_model_success(self, mock_session_factory: Any) -> None:
        """Test getting model when configured."""
        # Arrange
        repo = BaseRepository[User, UserSchema](mock_session_factory)
        repo.model = User

        # Act & Assert
        assert repo._get_model() == User

    def test_get_model_not_configured(self, mock_session_factory: Any) -> None:
        """Test getting model when not configured."""
        # Arrange
        repo = BaseRepository[User, UserSchema](mock_session_factory)
        repo.model = None

        # Act & Assert
        with pytest.raises(ValueError, match="Model not configured in repository"):
            repo._get_model()
