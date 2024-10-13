from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List
from uuid import UUID

from core.src.models.doctor_schedule import DoctorSchedule

from .base_repository import BaseRepository


class DoctorScheduleRepository(BaseRepository[DoctorSchedule], ABC):
    @abstractmethod
    async def get_by_doctor_id(self, doctor_id: UUID) -> List[DoctorSchedule]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_doctor_and_day(
        self, doctor_id: UUID, day_of_week: int
    ) -> List[DoctorSchedule]:
        raise NotImplementedError

    @abstractmethod
    async def get_available_slots(self, doctor_id: UUID, date: date) -> List[datetime]:
        raise NotImplementedError
