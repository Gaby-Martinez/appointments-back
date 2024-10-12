from dataclasses import replace
from datetime import date
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.doctor_memory_repository import (
    MemoryDoctorRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Doctor, Role, RoleEnum


async def test_create_doctor(
    doctor_repository: MemoryDoctorRepository, sample_doctor: Doctor
) -> None:
    created_doctor = await doctor_repository.create(sample_doctor)
    assert created_doctor.id == sample_doctor.id
    assert RoleEnum.DOCTOR in [role.name for role in created_doctor.roles]


async def test_create_doctor_missing_mandatory_fields(
    doctor_repository: MemoryDoctorRepository,
) -> None:
    with pytest.raises(TypeError):
        Doctor(  # type: ignore
            id=uuid4(),
            ci="1234567890",
            password="securepassword456",
            first_name="Test",
            last_name="User",
            phone_number="+1234567890",
            document_type="national_id",
            roles=[Role(name=RoleEnum.DOCTOR)],
            is_active=True,
        )


async def test_create_doctor_without_specialty_raises_Value_Error(
    doctor_repository: MemoryDoctorRepository,
) -> None:
    with pytest.raises(ValueError):
        Doctor(
            id=uuid4(),
            email="doctor@example.com",
            ci="9876543210",
            password="securepassword456",
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1990, 5, 15),
            phone_number="+1987654321",
            document_type="national_id",
            roles=[Role(name=RoleEnum.DOCTOR)],
            specialty=None,
            is_active=True,
        )


async def test_create_doctor_with_existing_ci(
    doctor_repository: MemoryDoctorRepository, sample_doctor: Doctor
) -> None:
    await doctor_repository.create(sample_doctor)
    duplicate_ci_doctor = replace(
        sample_doctor, id=uuid4(), email="new_doctor@example.com"
    )
    with pytest.raises(RepositoryOperationException):
        await doctor_repository.create(duplicate_ci_doctor)
