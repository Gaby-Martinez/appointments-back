from typing import List
from uuid import UUID, uuid4

import pytest

from adapters.src.repositories.memory.appointment_memory_repository import (
    MemoryAppointmentRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Appointment


async def test_create_appointment(
    appointment_repository: MemoryAppointmentRepository,
    sample_appointment_creation: Appointment,
):
    created_appointment = await appointment_repository.create(
        sample_appointment_creation
    )
    assert created_appointment.id is not None
    assert isinstance(created_appointment.id, UUID)

    retrieved_schedule = await appointment_repository.get_by_id(created_appointment.id)
    assert retrieved_schedule is not None
    assert retrieved_schedule == created_appointment


async def test_create_appointment_with_existing_id(
    appointment_repository: MemoryAppointmentRepository,
    sample_appointment: Appointment,
):
    existing_id = uuid4()
    sample_appointment.id = existing_id

    created_appointment = await appointment_repository.create(sample_appointment)
    assert created_appointment.id == existing_id

    retrieved_schedule = await appointment_repository.get_by_id(created_appointment.id)
    assert retrieved_schedule is not None
    assert retrieved_schedule == created_appointment


async def test_create_multiple_appointments(
    appointment_repository: MemoryAppointmentRepository,
    sample_weekly_appointments: List[Appointment],
):
    created_appointments: List[Appointment] = []

    for appointment in sample_weekly_appointments:
        created_appointment = await appointment_repository.create(appointment)
        created_appointments.append(created_appointment)

    assert len(created_appointments) == len(sample_weekly_appointments)

    for appointment in created_appointments:
        assert appointment.id is not None
        assert isinstance(appointment.id, UUID)

    all_appointments = await appointment_repository.list()
    assert len(all_appointments) == len(sample_weekly_appointments)
    assert set(app.id for app in all_appointments) == set(
        app.id for app in created_appointments
    )


async def test_repository_operation_exception_on_create(
    appointment_repository: MemoryAppointmentRepository,
    sample_appointment: Appointment,
):
    appointment_repository.appointments = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await appointment_repository.create(sample_appointment)

    assert "Appointment" in str(exc_info.value)
    assert "create" in str(exc_info.value)
