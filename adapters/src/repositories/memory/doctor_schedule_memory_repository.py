from dataclasses import replace
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import DoctorSchedule
from core.src.repositories.doctor_schedule_repository import DoctorScheduleRepository


class MemoryDoctorScheduleRepository(DoctorScheduleRepository):
    def __init__(self) -> None:
        self.schedules: Dict[UUID, DoctorSchedule] = {}

    async def create(self, doctor_schedule: DoctorSchedule) -> DoctorSchedule:
        try:
            if doctor_schedule.id is None:
                doctor_schedule = replace(doctor_schedule, id=uuid4())
            self.schedules[doctor_schedule.id] = doctor_schedule
            return doctor_schedule
        except Exception as e:
            raise RepositoryOperationException("DoctorSchedule", "create", str(e))

    async def get_by_id(
        self, doctor_schedule_id: UUID, include_inactive: bool = False
    ) -> Optional[DoctorSchedule]:
        try:
            schedule = self.schedules.get(doctor_schedule_id)
            if schedule and (include_inactive or schedule.is_active):
                return schedule
            return None
        except Exception as e:
            raise RepositoryOperationException("DoctorSchedule", "get_by_id", str(e))

    async def list(self, include_inactive: bool = False) -> List[DoctorSchedule]:
        try:
            if include_inactive:
                return list(self.schedules.values())
            return [
                schedule for schedule in self.schedules.values() if schedule.is_active
            ]
        except Exception as e:
            raise RepositoryOperationException("DoctorSchedule", "list", str(e))

    async def get_by_doctor_id(self, doctor_id: UUID) -> List[DoctorSchedule]:
        try:
            return [
                schedule
                for schedule in self.schedules.values()
                if schedule.doctor.id == doctor_id and schedule.is_active
            ]
        except Exception as e:
            raise RepositoryOperationException(
                "DoctorSchedule", "get_by_doctor_id", str(e)
            )

    async def get_by_doctor_and_day(
        self, doctor_id: UUID, day_of_week: int
    ) -> List[DoctorSchedule]:
        try:
            return [
                schedule
                for schedule in self.schedules.values()
                if schedule.doctor.id == doctor_id
                and schedule.day_of_week == day_of_week
                and schedule.is_active
            ]
        except Exception as e:
            raise RepositoryOperationException(
                "DoctorSchedule", "get_by_doctor_and_day", str(e)
            )

    async def get_available_slots(self, doctor_id: UUID, date: date) -> List[datetime]:
        try:
            day_of_week = date.weekday()
            schedules = await self.get_by_doctor_and_day(doctor_id, day_of_week)

            available_slots = []
            for schedule in schedules:
                current_time = datetime.combine(date, schedule.start_time)
                end_time = datetime.combine(date, schedule.end_time)
                while (
                    current_time + timedelta(minutes=schedule.appointment_duration)
                    <= end_time
                ):
                    available_slots.append(current_time)
                    current_time += timedelta(minutes=schedule.appointment_duration)

            return available_slots
        except Exception as e:
            raise RepositoryOperationException(
                "DoctorSchedule", "get_available_slots", str(e)
            )
