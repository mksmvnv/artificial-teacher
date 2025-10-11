import logging
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models.base import Base

logger = logging.getLogger(__name__)


class AbstractRepository[ModelType: Base, SchemaType: BaseModel](ABC):
    """Abstract repository."""

    @abstractmethod
    async def find_one_or_none(self, **filter_by_data: Any) -> ModelType | None:
        """Find one object or none."""
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: SchemaType) -> int:
        """Add one new object."""
        raise NotImplementedError


class BaseRepository[ModelType: Base, SchemaType: BaseModel](
    AbstractRepository[ModelType, SchemaType]
):
    """Base repository."""

    model: type[ModelType] | None = None

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    def _get_model(self) -> type[ModelType]:
        """Get model."""
        if self.model is None:
            raise ValueError(f"Model not configured in repository: {self.__class__.__name__}")
        return self.model

    async def find_one_or_none(self, **filter_by_data: Any) -> ModelType | None:
        """Find one object or none."""
        model = self._get_model()

        async with self.session_factory() as session:
            query = select(model).filter_by(**filter_by_data)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def add_one(self, data: SchemaType) -> int:
        """Add one new object."""
        model = self._get_model()

        async with self.session_factory() as session:
            instance = model(**data.model_dump())
            session.add(instance)
            await session.commit()
            return instance.id
