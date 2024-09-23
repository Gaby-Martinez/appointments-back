from abc import ABC, abstractmethod
from typing import List

from core.src.models.doctor import Doctor
from core.src.repositories.base_repository import BaseRepository


class DoctorRepository(BaseRepository[Doctor], ABC):
    @abstractmethod
    async def get_by_specialty(self, specialty_id: int) -> List[Doctor]:
        pass
