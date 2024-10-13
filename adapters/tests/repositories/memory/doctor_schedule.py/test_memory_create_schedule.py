from typing import List
from uuid import UUID, uuid4

import pytest

from adapters.src.repositories.memory.doctor_schedule_memory_repository import (
    MemoryDoctorScheduleRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import DoctorSchedule


async def test_create_doctor_schedule(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule_creation: DoctorSchedule,
):
    created_doctor_schedule = await doctor_schedule_repository.create(
        sample_doctor_schedule_creation
    )
    assert created_doctor_schedule.id is not None
    assert isinstance(created_doctor_schedule.id, UUID)

    retrieved_schedule = await doctor_schedule_repository.get_by_id(
        created_doctor_schedule.id
    )
    assert retrieved_schedule is not None
    assert retrieved_schedule == created_doctor_schedule


async def test_create_multiple_doctor_schedules(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_weekly_schedule: List[DoctorSchedule],
):
    created_schedules: List[DoctorSchedule] = []
    for schedule in sample_doctor_weekly_schedule:
        created_schedule = await doctor_schedule_repository.create(schedule)
        created_schedules.append(created_schedule)

    assert len(created_schedules) == len(sample_doctor_weekly_schedule)
    for schedule in created_schedules:
        assert schedule.id is not None
        assert isinstance(schedule.id, UUID)


async def test_create_doctor_schedule_with_existing_id(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
):
    existing_id = uuid4()
    sample_doctor_schedule.id = existing_id

    created_doctor_schedule = await doctor_schedule_repository.create(
        sample_doctor_schedule
    )
    assert created_doctor_schedule.id == existing_id

    retrieved_schedule = await doctor_schedule_repository.get_by_id(
        created_doctor_schedule.id
    )
    assert retrieved_schedule is not None
    assert retrieved_schedule == created_doctor_schedule


async def test_repository_operation_exception_on_create(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
):
    doctor_schedule_repository.schedules = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_schedule_repository.create(sample_doctor_schedule)

    assert "DoctorSchedule" in str(exc_info.value)
    assert "create" in str(exc_info.value)
