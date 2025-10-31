from unittest.mock import AsyncMock

import pytest

from src.schemas.user import UserSchema


@pytest.fixture
def fake_user() -> UserSchema:
    """Fake user with all fields."""
    return UserSchema(
        tg_id=123456789,
        username="fake_user",
        first_name="Ivan",
        last_name="Ivanov",
    )


@pytest.fixture
def fake_user_without_optional() -> UserSchema:
    """Fake user without optional fields."""
    return UserSchema(
        tg_id=123456790,
        username=None,
        first_name=None,
        last_name=None,
    )


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """Mock user repository for testing services."""
    return AsyncMock()
