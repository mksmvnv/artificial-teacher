import pytest
from pydantic import ValidationError

from src.schemas.user import UserSchema


class TestUserSchema:
    """Test UserSchema."""

    def test_create_valid_user(self, fake_user: UserSchema) -> None:
        """Test creating user with valid data."""
        assert fake_user.tg_id == 123456789
        assert fake_user.username == "fake_user"
        assert fake_user.first_name == "Ivan"
        assert fake_user.last_name == "Ivanov"

    def test_create_user_with_optional_fields_none(
        self, fake_user_without_optional: UserSchema
    ) -> None:
        """Test creating user with None optional fields."""
        assert fake_user_without_optional.tg_id == 123456790
        assert fake_user_without_optional.username is None
        assert fake_user_without_optional.first_name is None
        assert fake_user_without_optional.last_name is None

    def test_username_length_validation(self) -> None:
        """Test username length validation."""
        with pytest.raises(ValidationError):
            UserSchema(
                tg_id=123456789,
                username="a" * 33,  # 33 characters > 32 max_length
                first_name=None,
                last_name=None,
            )

    def test_first_name_length_validation(self) -> None:
        """Test first name length validation."""
        with pytest.raises(ValidationError):
            UserSchema(
                tg_id=123456789,
                username=None,
                first_name="a" * 65,  # 65 characters > 64 max_length
                last_name=None,
            )

    def test_last_name_length_validation(self) -> None:
        """Test last name length validation."""
        with pytest.raises(ValidationError):
            UserSchema(
                tg_id=123456789,
                username=None,
                first_name=None,
                last_name="a" * 65,  # 65 characters > 64 max_length
            )
