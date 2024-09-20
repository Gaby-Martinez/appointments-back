from abc import ABC, abstractmethod
from datetime import date
from typing import List

from core.src.models.appointment import Appointment
from core.src.repositories.base_repository import BaseRepository


class AppointmentRepository(BaseRepository[Appointment], ABC):
    @abstractmethod
    async def get_by_doctor_and_date(
        self, doctor_id: int, date: date
    ) -> List[Appointment]:
        pass

    @abstractmethod
    async def get_by_patient(self, patient_id: int) -> List[Appointment]:
        pass
