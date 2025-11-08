from typing import Any

import pytest

from src.schemas.user import UserSchema
from src.services import LanguageService


class TestLanguageService:
    """Test LanguageService class."""

    EN_LANG = "english"
    CN_LANG = "chinese"
    B1_CEFR_LEVEL = "b1"
    B2_CEFR_LEVEL = "b2"

    @pytest.mark.asyncio
    async def test_set_user_language_success(
        self,
        language_service: LanguageService,
        mock_user_repository_protocol: Any,
        fake_user: UserSchema,
    ) -> None:
        """Test successful language setting."""
        # Arrange
        mock_user_repository_protocol.find_by_user_tg_id.return_value = True
        mock_user_repository_protocol.get_user_language.return_value = self.EN_LANG

        # Act
        await language_service.set_user_language(fake_user.tg_id, self.CN_LANG)

        # Assert
        mock_user_repository_protocol.find_by_user_tg_id.assert_called_once_with(fake_user.tg_id)
        mock_user_repository_protocol.get_user_language.assert_called_once_with(
            user_tg_id=fake_user.tg_id
        )
        mock_user_repository_protocol.set_user_language.assert_called_once_with(
            language=self.CN_LANG, user_tg_id=fake_user.tg_id
        )

    @pytest.mark.asyncio
    async def test_set_user_language_user_not_found(
        self,
        language_service: LanguageService,
        mock_user_repository_protocol: Any,
        fake_user: UserSchema,
    ) -> None:
        """Test language setting when user not found."""
        # Arrange
        mock_user_repository_protocol.find_by_user_tg_id.return_value = None

        # Act
        await language_service.set_user_language(fake_user.tg_id, self.CN_LANG)

        # Assert
        mock_user_repository_protocol.find_by_user_tg_id.assert_called_once_with(fake_user.tg_id)
        mock_user_repository_protocol.get_user_language.assert_not_called()
        mock_user_repository_protocol.set_user_language.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_user_language_success(
        self,
        language_service: LanguageService,
        mock_user_repository_protocol: Any,
        fake_user: UserSchema,
    ) -> None:
        """Test successful language retrieval."""
        # Arrange
        mock_user_repository_protocol.find_by_user_tg_id.return_value = True
        mock_user_repository_protocol.get_user_language.return_value = self.EN_LANG

        # Act
        result = await language_service.get_user_language(fake_user.tg_id)

        # Assert
        assert result == self.EN_LANG
        mock_user_repository_protocol.find_by_user_tg_id.assert_called_once_with(fake_user.tg_id)
        mock_user_repository_protocol.get_user_language.assert_called_once_with(
            user_tg_id=fake_user.tg_id
        )

    @pytest.mark.asyncio
    async def test_set_user_cefr_level_success(
        self,
        language_service: LanguageService,
        mock_user_repository_protocol: Any,
        fake_user: UserSchema,
    ) -> None:
        """Test successful CEFR level setting."""
        # Arrange
        mock_user_repository_protocol.find_by_user_tg_id.return_value = True
        mock_user_repository_protocol.get_user_cefr_level.return_value = self.B1_CEFR_LEVEL

        # Act
        await language_service.set_user_cefr_level(fake_user.tg_id, self.B2_CEFR_LEVEL)

        # Assert
        mock_user_repository_protocol.find_by_user_tg_id.assert_called_once_with(fake_user.tg_id)
        mock_user_repository_protocol.get_user_cefr_level.assert_called_once_with(
            user_tg_id=fake_user.tg_id
        )
        mock_user_repository_protocol.set_user_cefr_level.assert_called_once_with(
            cefr_level=self.B2_CEFR_LEVEL, user_tg_id=fake_user.tg_id
        )
