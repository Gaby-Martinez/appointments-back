from datetime import datetime, time, timedelta
from typing import List
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.appointment_memory_repository import (
    MemoryAppointmentRepository,
)
from core.src.models import (
    Appointment,
    AppointmentStatus,
    AppointmentStatusEnum,
    Doctor,
    Patient,
)


@pytest.fixture
async def appointment_repository() -> MemoryAppointmentRepository:
    return MemoryAppointmentRepository()


@pytest.fixture
def sample_appointment_creation(
    sample_doctor: Doctor, sample_patient: Patient
) -> Appointment:
    return Appointment(
        id=None,  # type: ignore
        doctor=sample_doctor,
        patient=sample_patient,
        start_datetime=datetime.combine(datetime.now().date(), time(9, 0)),  # 9:00 AM
        duration=30,
        status=AppointmentStatus(name=AppointmentStatusEnum.SCHEDULED),
    )


@pytest.fixture
def sample_appointment(sample_doctor: Doctor, sample_patient: Patient) -> Appointment:
    return Appointment(
        id=uuid4(),
        doctor=sample_doctor,
        patient=sample_patient,
        start_datetime=datetime.combine(datetime.now().date(), time(9, 0)),  # 9:00 AM
        duration=30,
        status=AppointmentStatus(name=AppointmentStatusEnum.SCHEDULED),
    )


@pytest.fixture
def sample_weekly_appointments(
    sample_doctor: Doctor, sample_patient: Patient
) -> List[Appointment]:
    base_date = datetime.now().date()
    base_time = datetime.min.time().replace(hour=9)  # Start at 9 AM

    appointments = []
    for i in range(5):
        start_datetime = datetime.combine(base_date, base_time) + timedelta(days=i)
        appointments.append(
            Appointment(
                id=None,  # type: ignore
                doctor=sample_doctor,
                patient=sample_patient,
                start_datetime=start_datetime,
                duration=30,
                status=AppointmentStatus(name=AppointmentStatusEnum.SCHEDULED),
            )
        )

    return appointments
