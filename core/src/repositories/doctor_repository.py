from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from core.src.models import Doctor
from core.src.repositories.base_repository import BaseRepository


class DoctorRepository(BaseRepository[Doctor], ABC):
    @abstractmethod
    async def get_by_email(
        self, email: str, include_inactive: bool = False
    ) -> Optional[Doctor]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_ci(
        self, ci: str, include_inactive: bool = False
    ) -> Optional[Doctor]:
        raise NotImplementedError

    @abstractmethod
    async def get_doctors_by_specialty(self, specialty_id: UUID) -> List[Doctor]:
        raise NotImplementedError
