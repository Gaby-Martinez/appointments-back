from abc import ABC, abstractmethod
from typing import List, Optional

from core.src.models.specialty import Specialty

from .base_repository import BaseRepository


class SpecialtyRepository(BaseRepository[Specialty], ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Specialty]:
        pass

    @abstractmethod
    async def search_by_name(self, name_fragment: str) -> List[Specialty]:
        pass
