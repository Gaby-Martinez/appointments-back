from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from uuid import UUID

from core.src.models.appointment import Appointment
from core.src.repositories.base_repository import BaseRepository


class AppointmentRepository(BaseRepository[Appointment], ABC):
    @abstractmethod
    async def get_by_doctor_id(self, doctor_id: UUID) -> List[Appointment]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_patient_id(self, patient_id: UUID) -> List[Appointment]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Appointment]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_doctor_and_time_range(
        self, doctor_id: UUID, start_time: datetime, end_time: datetime
    ) -> List[Appointment]:
        raise NotImplementedError
