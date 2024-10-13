from datetime import time
from typing import List
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.doctor_schedule_memory_repository import (
    MemoryDoctorScheduleRepository,
)
from core.src.models import Doctor, DoctorSchedule


@pytest.fixture
async def doctor_schedule_repository() -> MemoryDoctorScheduleRepository:
    return MemoryDoctorScheduleRepository()


@pytest.fixture
def sample_doctor_schedule_creation(sample_doctor: Doctor) -> DoctorSchedule:
    return DoctorSchedule(
        id=None,  # type: ignore
        doctor=sample_doctor,
        day_of_week=0,  # Monday
        start_time=time(9, 0),  # 9:00 AM
        end_time=time(17, 0),  # 5:00 PM
        appointment_duration=30,
        is_active=True,
    )


@pytest.fixture
def sample_doctor_schedule(sample_doctor: Doctor) -> DoctorSchedule:
    return DoctorSchedule(
        id=uuid4(),
        doctor=sample_doctor,
        day_of_week=0,  # Monday
        start_time=time(9, 0),  # 9:00 AM
        end_time=time(17, 0),  # 5:00 PM
        appointment_duration=30,
        is_active=True,
    )


@pytest.fixture
def inactive_sample_doctor_schedule(sample_doctor: Doctor) -> DoctorSchedule:
    return DoctorSchedule(
        id=uuid4(),
        doctor=sample_doctor,
        day_of_week=0,  # Monday
        start_time=time(9, 0),  # 9:00 AM
        end_time=time(17, 0),  # 5:00 PM
        appointment_duration=30,
        is_active=False,
    )


@pytest.fixture
def sample_doctor_weekly_schedule(sample_doctor: Doctor) -> List[DoctorSchedule]:
    weekly_schedule = []
    for day in range(0, 5):
        schedule = DoctorSchedule(
            id=None,  # type: ignore
            doctor=sample_doctor,
            day_of_week=day,
            start_time=time(9, 0),
            end_time=time(17, 0),
            appointment_duration=30,
            is_active=True,
        )
        weekly_schedule.append(schedule)
    return weekly_schedule


@pytest.fixture
async def populated_repository(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
) -> MemoryDoctorScheduleRepository:
    await doctor_schedule_repository.create(sample_doctor_schedule)
    return doctor_schedule_repository
