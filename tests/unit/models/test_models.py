from src.models.base import Base
from src.models.user import User


class TestBaseModel:
    """Test Base model."""

    def test_base_model_abstract(self) -> None:
        """Test Base model is abstract."""
        assert Base.__abstract__ is True

    def test_base_model_has_required_columns(self) -> None:
        """Test Base model has required columns."""
        assert hasattr(Base, "id")
        assert hasattr(Base, "created_at")
        assert hasattr(Base, "updated_at")

    def test_base_tablename_generation(self) -> None:
        """Test table name generation."""

        class Test(Base):
            __abstract__ = False

        assert Test.__tablename__ == "tests"


class TestUserModel:
    """Test User model."""

    def test_user_model_table_name(self) -> None:
        """Test User model table name."""
        assert User.__tablename__ == "users"

    def test_user_model_columns(self) -> None:
        """Test User model has all required columns."""
        columns = [
            "id",
            "tg_id",
            "username",
            "first_name",
            "last_name",
            "is_admin",
            "language",
            "cefr_level",
            "created_at",
            "updated_at",
        ]

        for column in columns:
            assert hasattr(User, column)

    def test_user_model_defaults(self) -> None:
        """Test User model default values."""
        # Create user without optional fields
        user = User(tg_id=123456789)

        assert user.tg_id == 123456789
        assert hasattr(user, "is_admin")
        assert user.is_admin is None

    def test_user_model_boolean_field(self) -> None:
        """Test that is_admin field works correctly."""
        user_with_false = User(tg_id=123456789, is_admin=False)
        user_with_true = User(tg_id=123456790, is_admin=True)

        assert user_with_false.is_admin is False
        assert user_with_true.is_admin is True
