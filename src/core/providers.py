from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.database import async_session_maker
from src.repositories.user import UserRepository
from src.services import AssistantService, ContextService, LanguageService, StartService


class DatabaseProvider(Provider):
    """Database provider."""

    @provide(scope=Scope.APP)
    def provide_session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Provide session factory."""
        return async_session_maker


class RepositoryProvider(Provider):
    """Repository provider."""

    @provide(scope=Scope.REQUEST)
    def provide_user_repository(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> UserRepository:
        """Provide user repository."""
        return UserRepository(session_factory=session_factory)


class ServiceProvider(Provider):
    """Service provider."""

    @provide(scope=Scope.REQUEST)
    def provide_start_service(self, repository: UserRepository) -> StartService:
        """Provide start service."""
        return StartService(repository)

    @provide(scope=Scope.REQUEST)
    def provide_language_service(self, repository: UserRepository) -> LanguageService:
        """Provide language service."""
        return LanguageService(repository)

    @provide(scope=Scope.REQUEST)
    def provide_context_service(self) -> ContextService:
        """Provide context service."""
        return ContextService()

    @provide(scope=Scope.REQUEST)
    def provide_assistant_service(self) -> AssistantService:
        """Provide assistant service."""
        return AssistantService()
