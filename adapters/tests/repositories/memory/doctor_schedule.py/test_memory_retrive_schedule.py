from dataclasses import replace
from datetime import date, datetime, time
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.doctor_schedule_memory_repository import (
    MemoryDoctorScheduleRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import DoctorSchedule
from core.src.models.doctor import Doctor


async def test_get_by_id(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
):
    created_doctor_schedule = await doctor_schedule_repository.create(
        sample_doctor_schedule
    )
    retrieved_doctor_schedule = await doctor_schedule_repository.get_by_id(
        created_doctor_schedule.id
    )

    assert retrieved_doctor_schedule is not None

    assert retrieved_doctor_schedule.day_of_week == sample_doctor_schedule.day_of_week
    assert (
        retrieved_doctor_schedule.appointment_duration
        == sample_doctor_schedule.appointment_duration
    )
    assert retrieved_doctor_schedule.doctor == sample_doctor_schedule.doctor
    assert retrieved_doctor_schedule.end_time == sample_doctor_schedule.end_time
    assert retrieved_doctor_schedule.start_time == sample_doctor_schedule.start_time

    assert retrieved_doctor_schedule.id == created_doctor_schedule.id


async def test_get_by_id_not_found(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
):
    doctor_schedule = await doctor_schedule_repository.get_by_id(uuid4())
    assert doctor_schedule is None


async def test_get_by_id_no_doctor_schedules(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
):
    doctor_schedule = await doctor_schedule_repository.get_by_id(uuid4())
    assert doctor_schedule is None


async def test_inactive_doctor_schedule_retrieval(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
):
    inactive_doctor_schedule = replace(
        sample_doctor_schedule,
        is_active=False,
    )

    created_inactive_doctor_schedule = await doctor_schedule_repository.create(
        inactive_doctor_schedule
    )

    retrieved_doctor_schedule = await doctor_schedule_repository.get_by_id(
        created_inactive_doctor_schedule.id
    )
    assert retrieved_doctor_schedule is None

    retrieved_doctor_schedule = await doctor_schedule_repository.get_by_id(
        created_inactive_doctor_schedule.id, include_inactive=True
    )
    assert retrieved_doctor_schedule == created_inactive_doctor_schedule


async def test_get_by_doctor_id(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
):
    created_doctor_schedule = await doctor_schedule_repository.create(
        sample_doctor_schedule
    )
    retrieved_doctor_schedule = await doctor_schedule_repository.get_by_doctor_id(
        sample_doctor_schedule.doctor.id
    )
    assert retrieved_doctor_schedule == [created_doctor_schedule]


async def test_get_by_doctor_and_day(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
):
    created_doctor_schedule = await doctor_schedule_repository.create(
        sample_doctor_schedule
    )
    retrieved_doctor_schedule = await doctor_schedule_repository.get_by_doctor_and_day(
        sample_doctor_schedule.doctor.id, 0
    )
    assert retrieved_doctor_schedule == [created_doctor_schedule]


async def test_get_available_slots(
    populated_repository: MemoryDoctorScheduleRepository,
    sample_doctor_schedule: DoctorSchedule,
):
    test_date = date(2024, 1, 1)  # A Monday
    slots = await populated_repository.get_available_slots(
        sample_doctor_schedule.doctor.id, test_date
    )

    assert len(slots) > 0
    assert all(isinstance(slot, datetime) for slot in slots)
    assert all(slot.date() == test_date for slot in slots)

    assert all(
        time(slot.hour, slot.minute) >= sample_doctor_schedule.start_time
        for slot in slots
    )
    assert all(
        time(slot.hour, slot.minute) < sample_doctor_schedule.end_time for slot in slots
    )

    expected_slots = (
        sample_doctor_schedule.end_time.hour - sample_doctor_schedule.start_time.hour
    ) * (60 // sample_doctor_schedule.appointment_duration)
    assert len(slots) == expected_slots

    for i in range(1, len(slots)):
        assert (
            slots[i] - slots[i - 1]
        ).total_seconds() / 60 == sample_doctor_schedule.appointment_duration


async def test_get_by_doctor_and_day_no_schedule(
    populated_repository: MemoryDoctorScheduleRepository,
    sample_doctor: Doctor,
):
    schedules = await populated_repository.get_by_doctor_and_day(
        sample_doctor.id, 1
    )  # Tuesday
    assert len(schedules) == 0


async def test_get_available_slots_no_schedule(
    populated_repository: MemoryDoctorScheduleRepository,
    sample_doctor: Doctor,
):
    test_date = date(2024, 1, 2)  # A Tuesday
    slots = await populated_repository.get_available_slots(sample_doctor.id, test_date)
    assert len(slots) == 0


async def test_repository_operation_exception_on_get_by_id(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
):
    doctor_schedule_repository.schedules = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_schedule_repository.get_by_id(uuid4())

    assert "DoctorSchedule" in str(exc_info.value)
    assert "get_by_id" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_doctor_id(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
):
    doctor_schedule_repository.schedules = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_schedule_repository.get_by_doctor_id(uuid4())

    assert "DoctorSchedule" in str(exc_info.value)
    assert "get_by_doctor_id" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_doctor_and_day(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
):
    doctor_schedule_repository.schedules = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_schedule_repository.get_by_doctor_and_day(uuid4(), 1)

    assert "DoctorSchedule" in str(exc_info.value)
    assert "get_by_doctor_and_day" in str(exc_info.value)


async def test_repository_operation_exception_on_get_available_slots(
    doctor_schedule_repository: MemoryDoctorScheduleRepository,
):
    doctor_schedule_repository.schedules = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_schedule_repository.get_available_slots(uuid4(), date(2024, 1, 2))

    assert "DoctorSchedule" in str(exc_info.value)
    assert "get_available_slots" in str(exc_info.value)
