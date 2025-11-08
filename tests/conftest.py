from typing import Any
from unittest.mock import MagicMock, create_autospec

import pytest
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models.user import User
from src.repositories.user import UserRepository, UserRepositoryProtocol
from src.schemas.user import UserSchema
from src.services import LanguageService, StartService


@pytest.fixture
def fake_user() -> UserSchema:
    """Fake user schema with all fields."""
    return UserSchema(
        tg_id=123456789,
        username="fake_user",
        first_name="Ivan",
        last_name="Ivanov",
    )


@pytest.fixture
def fake_user_without_optional() -> UserSchema:
    """Fake user schema without optional fields."""
    return UserSchema(
        tg_id=123456790,
        username=None,
        first_name=None,
        last_name=None,
    )


@pytest.fixture
def mock_user_repository_protocol() -> Any:
    """Create autospecced user repository protocol."""
    return create_autospec(UserRepositoryProtocol)


@pytest.fixture
def start_service(mock_user_repository_protocol: Any) -> StartService:
    """Create StartService with autospecced repository."""
    return StartService(user_repository=mock_user_repository_protocol)


@pytest.fixture
def language_service(mock_user_repository_protocol: Any) -> LanguageService:
    """Create LanguageService with autospecced repository."""
    return LanguageService(user_repository=mock_user_repository_protocol)


@pytest.fixture
def mock_async_session() -> Any:
    """Create mock async session."""
    session = create_autospec(AsyncSession, instance=True)

    mock_result = MagicMock(spec=Result)
    session.execute.return_value = mock_result

    return session


@pytest.fixture
def mock_session_factory(mock_async_session: Any) -> Any:
    """Create mock session factory."""
    factory = create_autospec(async_sessionmaker[AsyncSession], instance=True)
    factory.return_value.__aenter__.return_value = mock_async_session
    factory.return_value.__aexit__.return_value = None
    return factory


@pytest.fixture
def mock_user_repository(mock_session_factory: Any) -> UserRepository:
    """Create UserRepository with mocked session factory."""
    return UserRepository(session_factory=mock_session_factory)


@pytest.fixture
def user_model(fake_user: UserSchema) -> User:
    """Create User model from schema."""
    return User(
        tg_id=fake_user.tg_id,
        username=fake_user.username,
        first_name=fake_user.first_name,
        last_name=fake_user.last_name,
        language="english",
        cefr_level="b1",
    )
