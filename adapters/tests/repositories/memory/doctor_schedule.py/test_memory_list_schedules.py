from dataclasses import replace
from datetime import time
from typing import List
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.doctor_schedule_memory_repository import (
    MemoryDoctorScheduleRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import DoctorSchedule


@pytest.mark.asyncio
async def test_list_doctor_schedules(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_weekly_schedule: List[DoctorSchedule],
):
    created_schedules = []
    for schedule in sample_doctor_weekly_schedule:
        created_schedule = await doctor_schedule_repository.create(schedule)
        created_schedules.append(created_schedule)

    doctor_schedules_list = await doctor_schedule_repository.list()

    assert len(doctor_schedules_list) == len(sample_doctor_weekly_schedule)

    for created_schedule in created_schedules:
        assert created_schedule in doctor_schedules_list

    # Optional: Assert that the schedules are for different days
    days = [schedule.day_of_week for schedule in doctor_schedules_list]
    assert len(set(days)) == len(days), "All schedules should be for different days"


async def test_list_doctor_schedules_with_inactive(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
    inactive_sample_doctor_schedule: DoctorSchedule,
):
    active_doctor_schedule = await doctor_schedule_repository.create(
        sample_doctor_schedule
    )

    await doctor_schedule_repository.create(inactive_sample_doctor_schedule)

    active_doctor_schedules = await doctor_schedule_repository.list(
        include_inactive=False
    )

    all_doctor_schedules = await doctor_schedule_repository.list(include_inactive=True)

    assert len(active_doctor_schedules) == 1
    assert active_doctor_schedule in active_doctor_schedules
    assert inactive_sample_doctor_schedule not in active_doctor_schedules

    assert len(all_doctor_schedules) == 2
    assert active_doctor_schedule in all_doctor_schedules
    assert inactive_sample_doctor_schedule in all_doctor_schedules


async def test_list_excludes_inactive_doctor_schedules(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    inactive_sample_doctor_schedule: DoctorSchedule,
):
    await doctor_schedule_repository.create(inactive_sample_doctor_schedule)

    active_doctor_schedules = await doctor_schedule_repository.list(
        include_inactive=False
    )
    assert len(active_doctor_schedules) == 0


async def test_list_with_active_and_inactive_doctor_schedules(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
    inactive_sample_doctor_schedule: DoctorSchedule,
):
    doctor_schedules = [
        sample_doctor_schedule,
        replace(
            sample_doctor_schedule,
            id=uuid4(),
            day_of_week=1,  # Monday
            start_time=time(9, 0),  # 9:00 AM
            end_time=time(17, 0),  # 5:00 PM
        ),
        replace(
            inactive_sample_doctor_schedule,
            id=uuid4(),
            day_of_week=2,  # Tuesday
            start_time=time(9, 0),  # 9:00 AM
            end_time=time(17, 0),  # 5:00 PM
        ),
    ]

    for doctor_schedule in doctor_schedules:
        await doctor_schedule_repository.create(doctor_schedule)

    all_doctor_schedules = await doctor_schedule_repository.list(include_inactive=True)
    active_doctor_schedules = await doctor_schedule_repository.list(
        include_inactive=False
    )

    assert len(all_doctor_schedules) == 3
    assert len(active_doctor_schedules) == 2


async def test_list_no_doctor_schedules(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
):
    doctor_schedules = await doctor_schedule_repository.list()
    assert doctor_schedules == []


async def test_repository_operation_exception_on_list(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
):
    doctor_schedule_repository.schedules = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_schedule_repository.list()

    assert "DoctorSchedule" in str(exc_info.value)
    assert "list" in str(exc_info.value)
