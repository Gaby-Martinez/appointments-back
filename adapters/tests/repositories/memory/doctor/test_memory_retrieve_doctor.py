from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.doctor_memory_repository import (
    MemoryDoctorRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Doctor


async def test_get_doctor_by_id(
    doctor_repository: MemoryDoctorRepository, sample_doctor: Doctor
) -> None:
    await doctor_repository.create(sample_doctor)
    retrieved_doctor = await doctor_repository.get_by_id(sample_doctor.id)
    assert retrieved_doctor is not None
    assert retrieved_doctor.email == sample_doctor.email


async def test_get_doctor_by_email(
    doctor_repository: MemoryDoctorRepository, sample_doctor: Doctor
) -> None:
    await doctor_repository.create(sample_doctor)
    retrieved_doctor = await doctor_repository.get_by_email(sample_doctor.email)
    assert retrieved_doctor is not None
    assert retrieved_doctor.id == sample_doctor.id


async def test_get_doctor_by_ci(
    doctor_repository: MemoryDoctorRepository, sample_doctor: Doctor
) -> None:
    await doctor_repository.create(sample_doctor)
    retrieved_doctor = await doctor_repository.get_by_ci(sample_doctor.ci)
    assert retrieved_doctor is not None
    assert retrieved_doctor.id == sample_doctor.id


async def test_get_non_existent_doctor(
    doctor_repository: MemoryDoctorRepository,
) -> None:
    non_existent_id = uuid4()
    retrieved_doctor = await doctor_repository.get_by_id(non_existent_id)
    assert retrieved_doctor is None


async def test_repository_operation_exception_on_get_by_id(
    doctor_repository: MemoryDoctorRepository,
):
    doctor_repository.doctors = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_repository.get_by_id(uuid4())

    assert "Doctor" in str(exc_info.value)
    assert "get_by_id" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_email(
    doctor_repository: MemoryDoctorRepository,
):
    doctor_repository.user_repository = AsyncMock()
    mock_user = AsyncMock()
    mock_user.id = "some-unique-id"
    doctor_repository.user_repository.get_by_email.return_value = mock_user

    doctor_repository.doctors = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_repository.get_by_email("test@example.com")

    assert "Doctor" in str(exc_info.value)
    assert "get_by_email" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_ci(
    doctor_repository: MemoryDoctorRepository,
):
    doctor_repository.user_repository = AsyncMock()
    mock_user = AsyncMock()
    mock_user.ci = "some-unique-id"
    doctor_repository.user_repository.get_by_ci.return_value = mock_user

    doctor_repository.doctors = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_repository.get_by_ci("123214")

    assert "Doctor" in str(exc_info.value)
    assert "get_by_ci" in str(exc_info.value)
