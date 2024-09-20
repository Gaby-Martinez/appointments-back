from abc import ABC

from core.src.models.patient import Patient
from core.src.repositories.base_repository import BaseRepository


class PatientRepository(BaseRepository[Patient], ABC):
    pass
