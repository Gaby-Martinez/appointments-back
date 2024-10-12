from dataclasses import replace
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Specialty
from core.src.repositories.specialty_repository import SpecialtyRepository


class MemorySpecialtyRepository(SpecialtyRepository):
    def __init__(self) -> None:
        self.specialties: Dict[UUID, Specialty] = {}

    async def create(self, specialty: Specialty) -> Specialty:
        try:
            if specialty.id is None:
                specialty = replace(specialty, id=uuid4())

            self.specialties[specialty.id] = specialty

            return specialty
        except Exception as e:
            raise RepositoryOperationException("Specialty", "create", str(e))

    async def get_by_id(
        self, specialty_id: UUID, include_inactive: bool = False
    ) -> Optional[Specialty]:
        try:
            specialty = self.specialties.get(specialty_id)
            if specialty and (include_inactive or specialty.is_active):
                return specialty
            return None
        except Exception as e:
            raise RepositoryOperationException("Specialty", "get_by_id", str(e))

    async def list(self, include_inactive: bool = False) -> List[Specialty]:
        try:
            if include_inactive:
                return list(self.specialties.values())
            return [
                specialty
                for specialty in self.specialties.values()
                if specialty.is_active
            ]
        except Exception as e:
            raise RepositoryOperationException("Specialty", "list", str(e))
