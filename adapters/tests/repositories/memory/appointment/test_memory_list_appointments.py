from dataclasses import replace
from datetime import datetime, time, timedelta
from typing import List
from uuid import UUID, uuid4

import pytest

from adapters.src.repositories.memory.appointment_memory_repository import (
    MemoryAppointmentRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Appointment, Doctor


async def test_list_appointments(
    appointment_repository: MemoryAppointmentRepository,
    sample_weekly_appointments: List[Appointment],
):
    created_appointments = []
    for appointment in sample_weekly_appointments:
        created_appointment = await appointment_repository.create(appointment)
        created_appointments.append(created_appointment)

    appointments_list = await appointment_repository.list()

    assert len(appointments_list) == len(sample_weekly_appointments)

    for created_appointment in created_appointments:
        assert created_appointment in appointments_list


async def test_list_no_appointments(
    appointment_repository: MemoryAppointmentRepository,
):
    appointments = await appointment_repository.list()
    assert appointments == []


async def test_list_get_by_doctor_id(
    appointment_repository: MemoryAppointmentRepository,
    sample_weekly_appointments: List[Appointment],
):
    created_appointments = []
    for appointment in sample_weekly_appointments:
        created_appointment = await appointment_repository.create(appointment)
        created_appointments.append(created_appointment)

    doctor_id = sample_weekly_appointments[0].doctor.id
    appointments_list = await appointment_repository.get_by_doctor_id(doctor_id)

    assert all(appointment.doctor.id == doctor_id for appointment in appointments_list)

    assert len(appointments_list) == len(created_appointments)


async def test_list_get_by_patient_id(
    appointment_repository: MemoryAppointmentRepository,
    sample_weekly_appointments: List[Appointment],
):
    created_appointments = []
    for appointment in sample_weekly_appointments:
        created_appointment = await appointment_repository.create(appointment)
        created_appointments.append(created_appointment)

    patient_id = sample_weekly_appointments[0].patient.id
    appointments_list = await appointment_repository.get_by_patient_id(patient_id)

    assert all(
        appointment.patient.id == patient_id for appointment in appointments_list
    )

    assert len(appointments_list) == len(created_appointments)


async def test_get_by_date_range(
    appointment_repository: MemoryAppointmentRepository,
    sample_weekly_appointments: List[Appointment],
):
    for appointment in sample_weekly_appointments:
        await appointment_repository.create(appointment)

    start_date = sample_weekly_appointments[1].start_datetime
    end_date = sample_weekly_appointments[3].start_datetime + timedelta(hours=1)

    appointments_in_range = await appointment_repository.get_by_date_range(
        start_date, end_date
    )

    assert len(appointments_in_range) == 3
    for appointment in appointments_in_range:
        assert start_date <= appointment.start_datetime < end_date

    exact_start = await appointment_repository.get_by_date_range(
        sample_weekly_appointments[0].start_datetime,
        sample_weekly_appointments[0].start_datetime + timedelta(minutes=1),
    )
    assert len(exact_start) == 1

    exact_end = await appointment_repository.get_by_date_range(
        sample_weekly_appointments[0].start_datetime,
        sample_weekly_appointments[1].start_datetime,
    )
    assert len(exact_end) == 1


async def test_get_by_doctor_and_time_range(
    appointment_repository: MemoryAppointmentRepository,
    sample_weekly_appointments: List[Appointment],
    sample_doctor: Doctor,
):
    for appointment in sample_weekly_appointments:
        await appointment_repository.create(appointment)

    different_doctor = replace(
        sample_doctor, id=UUID("12345678-1234-5678-1234-567812345678")
    )
    different_doctor_appointment = replace(
        sample_weekly_appointments[2],
        id=None,  # type: ignore
        doctor=different_doctor,
        start_datetime=sample_weekly_appointments[2].start_datetime
        + timedelta(minutes=30),
    )
    await appointment_repository.create(different_doctor_appointment)

    start_time = sample_weekly_appointments[1].start_datetime
    end_time = sample_weekly_appointments[3].start_datetime + timedelta(hours=1)

    appointments = await appointment_repository.get_by_doctor_and_time_range(
        sample_doctor.id, start_time, end_time
    )

    assert len(appointments) == 3
    for appointment in appointments:
        assert appointment.doctor.id == sample_doctor.id
        assert appointment.start_datetime < end_time
        assert (
            appointment.start_datetime + timedelta(minutes=appointment.duration)
        ) > start_time

    assert all(
        appointment.id != different_doctor_appointment.id
        for appointment in appointments
    )


async def test_repository_operation_exception_on_list(
    appointment_repository: MemoryAppointmentRepository,
):
    appointment_repository.appointments = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await appointment_repository.list()

    assert "Appointment" in str(exc_info.value)
    assert "list" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_doctor_id(
    appointment_repository: MemoryAppointmentRepository,
):
    appointment_repository.appointments = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await appointment_repository.get_by_doctor_id(uuid4())

    assert "Appointment" in str(exc_info.value)
    assert "get_by_doctor_id" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_patient_id(
    appointment_repository: MemoryAppointmentRepository,
):
    appointment_repository.appointments = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await appointment_repository.get_by_patient_id(uuid4())

    assert "Appointment" in str(exc_info.value)
    assert "get_by_patient_id" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_date_range(
    appointment_repository: MemoryAppointmentRepository,
):
    appointment_repository.appointments = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await appointment_repository.get_by_date_range(
            datetime.combine(datetime.now().date(), time(9, 0)),
            datetime.combine(datetime.now().date(), time(9, 30)),
        )

    assert "Appointment" in str(exc_info.value)
    assert "get_by_date_range" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_doctor_and_time_range(
    appointment_repository: MemoryAppointmentRepository,
):
    appointment_repository.appointments = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await appointment_repository.get_by_doctor_and_time_range(
            uuid4(),
            datetime.combine(datetime.now().date(), time(9, 0)),
            datetime.combine(datetime.now().date(), time(9, 30)),
        )

    assert "Appointment" in str(exc_info.value)
    assert "get_by_doctor_and_time_range" in str(exc_info.value)
