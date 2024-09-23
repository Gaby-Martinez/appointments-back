from abc import ABC, abstractmethod
from typing import List

from core.src.models.doctor_schedule import DoctorSchedule

from .base_repository import BaseRepository


class DoctorScheduleRepository(BaseRepository[DoctorSchedule], ABC):
    @abstractmethod
    async def get_by_doctor_id(self, doctor_id: int) -> List[DoctorSchedule]:
        pass

    @abstractmethod
    async def get_by_day_of_week(self, day_of_week: int) -> List[DoctorSchedule]:
        pass
