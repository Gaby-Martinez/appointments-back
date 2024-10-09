from datetime import date
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.patient_memory_repository import (
    MemoryPatientRepository,
)
from adapters.src.repositories.memory.user_memory_repository import MemoryUserRepository
from core.src.models import Patient, Role, RoleEnum


@pytest.fixture
def patient_repository(
    user_repository: MemoryUserRepository,
) -> MemoryPatientRepository:
    return MemoryPatientRepository(user_repository)


@pytest.fixture
def sample_patient() -> Patient:
    return Patient(
        id=uuid4(),
        email="patient@example.com",
        ci="9876543210",
        password="securepassword456",
        first_name="Jane",
        last_name="Doe",
        date_of_birth=date(1990, 5, 15),
        phone_number="+1987654321",
        document_type="national_id",
        roles=[Role(name=RoleEnum.PATIENT)],
        is_active=True,
    )


@pytest.fixture
def inactive_sample_patient() -> Patient:
    return Patient(
        id=uuid4(),
        email="inactive_patient@example.com",
        ci="1234567890",
        password="securepassword789",
        first_name="John",
        last_name="Smith",
        date_of_birth=date(1985, 3, 22),
        phone_number="+1234567890",
        document_type="national_id",
        roles=[Role(name=RoleEnum.PATIENT)],
        is_active=False,
    )
