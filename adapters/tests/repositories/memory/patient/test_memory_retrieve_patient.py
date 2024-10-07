from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.patient_memory_repository import (
    MemoryPatientRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models.patient import Patient


async def test_get_patient_by_id(
    patient_repository: MemoryPatientRepository, sample_patient: Patient
) -> None:
    await patient_repository.create(sample_patient)
    retrieved_patient = await patient_repository.get_by_id(sample_patient.id)
    assert retrieved_patient is not None
    assert retrieved_patient.email == sample_patient.email


async def test_get_patient_by_email(
    patient_repository: MemoryPatientRepository, sample_patient: Patient
) -> None:
    await patient_repository.create(sample_patient)
    retrieved_patient = await patient_repository.get_by_email(sample_patient.email)
    assert retrieved_patient is not None
    assert retrieved_patient.id == sample_patient.id


async def test_get_patient_by_ci(
    patient_repository: MemoryPatientRepository, sample_patient: Patient
) -> None:
    await patient_repository.create(sample_patient)
    retrieved_patient = await patient_repository.get_by_ci(sample_patient.ci)
    assert retrieved_patient is not None
    assert retrieved_patient.id == sample_patient.id


async def test_get_non_existent_patient(
    patient_repository: MemoryPatientRepository,
) -> None:
    non_existent_id = uuid4()
    retrieved_patient = await patient_repository.get_by_id(non_existent_id)
    assert retrieved_patient is None


async def test_repository_operation_exception_on_get_by_id(
    patient_repository: MemoryPatientRepository,
):
    patient_repository.patients = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await patient_repository.get_by_id(uuid4())

    assert "Patient" in str(exc_info.value)
    assert "get_by_id" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_email(
    patient_repository: MemoryPatientRepository,
):
    patient_repository.user_repository = AsyncMock()
    mock_user = AsyncMock()
    mock_user.id = "some-unique-id"
    patient_repository.user_repository.get_by_email.return_value = mock_user

    patient_repository.patients = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await patient_repository.get_by_email("test@example.com")

    assert "Patient" in str(exc_info.value)
    assert "get_by_email" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_ci(
    patient_repository: MemoryPatientRepository,
):
    patient_repository.user_repository = AsyncMock()
    mock_user = AsyncMock()
    mock_user.ci = "some-unique-id"
    patient_repository.user_repository.get_by_ci.return_value = mock_user

    patient_repository.patients = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await patient_repository.get_by_ci("123214")

    assert "Patient" in str(exc_info.value)
    assert "get_by_ci" in str(exc_info.value)
