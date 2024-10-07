from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self, entity_id: UUID, include_inactive: bool = False
    ) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def list(self, include_inactive: bool = False) -> List[T]:
        raise NotImplementedError

    async def update(self, entity: T) -> T:
        raise NotImplementedError("Update operation is not implemented")

    async def delete(self, entity_id: UUID) -> bool:
        raise NotImplementedError("Delete operation is not implemented")

    async def restore(self, entity_id: UUID) -> bool:
        raise NotImplementedError("Restore operation is not implemented")
