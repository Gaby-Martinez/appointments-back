from uuid import uuid4

import pytest

from adapters.src.repositories.memory.appointment_memory_repository import (
    MemoryAppointmentRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Appointment


async def test_get_by_id(
    appointment_repository: MemoryAppointmentRepository,
    sample_appointment: Appointment,
):
    created_appointment = await appointment_repository.create(sample_appointment)
    retrieved_appointment = await appointment_repository.get_by_id(
        created_appointment.id
    )

    assert retrieved_appointment is not None

    assert retrieved_appointment.doctor == sample_appointment.doctor
    assert retrieved_appointment.patient == sample_appointment.patient
    assert retrieved_appointment.start_datetime == sample_appointment.start_datetime
    assert retrieved_appointment.duration == sample_appointment.duration
    assert retrieved_appointment.status == sample_appointment.status

    assert retrieved_appointment.id == created_appointment.id


async def test_get_by_id_not_found(
    appointment_repository: MemoryAppointmentRepository,
):
    appointment = await appointment_repository.get_by_id(uuid4())
    assert appointment is None


async def test_get_by_id_no_appointments(
    appointment_repository: MemoryAppointmentRepository,
):
    appointment = await appointment_repository.get_by_id(uuid4())
    assert appointment is None


async def test_get_by_doctor_id(
    appointment_repository: MemoryAppointmentRepository,
    sample_appointment: Appointment,
):
    created_appointment = await appointment_repository.create(sample_appointment)
    retrieved_appointment = await appointment_repository.get_by_doctor_id(
        sample_appointment.doctor.id
    )
    assert retrieved_appointment == [created_appointment]


async def test_repository_operation_exception_on_get_by_id(
    appointment_repository: MemoryAppointmentRepository,
):
    appointment_repository.appointments = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await appointment_repository.get_by_id(uuid4())

    assert "Appointment" in str(exc_info.value)
    assert "get_by_id" in str(exc_info.value)
