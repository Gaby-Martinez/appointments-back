from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        pass

    @abstractmethod
    async def list(self) -> List[T]:
        pass
