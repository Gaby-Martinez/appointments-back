from dataclasses import replace
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.patient_memory_repository import (
    MemoryPatientRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Patient, Role, RoleEnum


async def test_create_patient(
    patient_repository: MemoryPatientRepository, sample_patient: Patient
) -> None:
    created_patient = await patient_repository.create(sample_patient)
    assert created_patient.id == sample_patient.id
    assert RoleEnum.PATIENT in [role.name for role in created_patient.roles]


async def test_create_patient_missing_mandatory_fields(
    patient_repository: MemoryPatientRepository,
) -> None:
    with pytest.raises(TypeError):
        Patient(  # type: ignore
            id=uuid4(),
            ci="1234567890",
            password="securepassword456",
            first_name="Test",
            last_name="User",
            phone_number="+1234567890",
            document_type="national_id",
            roles=[Role(name=RoleEnum.PATIENT)],
            is_active=True,
        )


async def test_create_patient_with_existing_ci(
    patient_repository: MemoryPatientRepository, sample_patient: Patient
) -> None:
    await patient_repository.create(sample_patient)
    duplicate_ci_patient = replace(
        sample_patient, id=uuid4(), email="new_patient@example.com"
    )
    with pytest.raises(RepositoryOperationException):
        await patient_repository.create(duplicate_ci_patient)
