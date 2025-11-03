from typing import Any
from unittest.mock import MagicMock

import pytest
from sqlalchemy import select, update
from sqlalchemy.engine import Result

from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import UserSchema


class TestUserRepository:
    """Test UserRepository class."""

    NONEXISTENT_USER_TG_ID = 987654321
    EN_LANG = "EN"
    B1_CEFR_LEVEL = "B1"

    @pytest.mark.asyncio
    async def test_find_by_tg_id_found(
        self,
        mock_user_repository: UserRepository,
        mock_async_session: Any,
        user_model: User,
        fake_user: UserSchema,
    ) -> None:
        """Test finding user by tg_id when exists."""
        # Arrange
        mock_result = MagicMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = user_model
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await mock_user_repository.find_by_tg_id(user_model.tg_id)

        assert result == fake_user
        mock_async_session.execute.assert_called_once()
        call_args = mock_async_session.execute.call_args[0][0]
        assert str(call_args) == str(select(User).filter_by(tg_id=user_model.tg_id))

    @pytest.mark.asyncio
    async def test_find_by_tg_id_not_found(
        self, mock_user_repository: UserRepository, mock_async_session: Any
    ) -> None:
        """Test finding user by tg_id when not exists."""
        # Arrange
        mock_result = MagicMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await mock_user_repository.find_by_tg_id(self.NONEXISTENT_USER_TG_ID)

        # Assert
        assert result is None
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_language_found(
        self, mock_user_repository: UserRepository, mock_async_session: Any, user_model: User
    ) -> None:
        """Test getting user language when user exists."""
        # Arrange
        mock_result = MagicMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = user_model
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await mock_user_repository.get_user_language(user_model.tg_id)

        # Assert
        assert result == user_model.language
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_language_not_found(
        self, mock_user_repository: UserRepository, mock_async_session: Any
    ) -> None:
        """Test getting user language when user not exists."""
        # Arrange
        mock_result = MagicMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await mock_user_repository.get_user_language(self.NONEXISTENT_USER_TG_ID)

        # Assert
        assert result is None
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_user_language(
        self, mock_user_repository: UserRepository, mock_async_session: Any
    ) -> None:
        """Test setting user language."""
        # Arrange
        mock_result = MagicMock(spec=Result)
        mock_async_session.execute.return_value = mock_result

        # Act
        await mock_user_repository.set_user_language(self.EN_LANG, self.NONEXISTENT_USER_TG_ID)

        # Assert
        mock_async_session.execute.assert_called_once()
        call_args = mock_async_session.execute.call_args[0][0]
        expected_query = (
            update(User).filter_by(tg_id=self.NONEXISTENT_USER_TG_ID).values(language=self.EN_LANG)
        )
        assert str(call_args) == str(expected_query)
        mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_cefr_level_found(
        self, mock_user_repository: UserRepository, mock_async_session: Any, user_model: User
    ) -> None:
        """Test getting user CEFR level when user exists."""
        # Arrange
        mock_result = MagicMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = user_model
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await mock_user_repository.get_user_cefr_level(user_model.tg_id)

        # Assert
        assert result == user_model.cefr_level
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_cefr_level_not_found(
        self, mock_user_repository: UserRepository, mock_async_session: Any
    ) -> None:
        """Test getting user CEFR level when user not exists."""
        # Arrange
        mock_result = MagicMock(spec=Result)
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute.return_value = mock_result

        # Act
        result = await mock_user_repository.get_user_cefr_level(self.NONEXISTENT_USER_TG_ID)

        # Assert
        assert result is None
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_user_cefr_level(
        self, mock_user_repository: UserRepository, mock_async_session: Any
    ) -> None:
        """Test setting user CEFR level."""
        # Arrange
        mock_result = MagicMock(spec=Result)
        mock_async_session.execute.return_value = mock_result

        # Act
        await mock_user_repository.set_user_cefr_level(
            self.B1_CEFR_LEVEL, self.NONEXISTENT_USER_TG_ID
        )

        # Assert
        mock_async_session.execute.assert_called_once()
        call_args = mock_async_session.execute.call_args[0][0]
        expected_query = (
            update(User)
            .filter_by(tg_id=self.NONEXISTENT_USER_TG_ID)
            .values(cefr_level=self.B1_CEFR_LEVEL)
        )
        assert str(call_args) == str(expected_query)
        mock_async_session.commit.assert_called_once()

    def test_user_repository_inheritance(self, mock_session_factory: Any) -> None:
        """Test that UserRepository correctly inherits from BaseRepository."""
        # Act
        repo = UserRepository(session_factory=mock_session_factory)

        # Assert
        assert isinstance(repo, UserRepository)
        assert hasattr(repo, "model")
        assert repo.model == User
        assert hasattr(repo, "session_factory")
