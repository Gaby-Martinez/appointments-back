from uuid import UUID, uuid4

import pytest

from adapters.src.repositories.memory.specialty_memory_repository import (
    MemorySpecialtyRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Specialty


async def test_create_specialty(
    specialty_repository: MemorySpecialtyRepository,
    sample_specialty_creation: Specialty,
):
    created_specialty = await specialty_repository.create(sample_specialty_creation)
    assert created_specialty.id is not None
    assert isinstance(created_specialty.id, UUID)
    assert (
        await specialty_repository.get_by_id(created_specialty.id) == created_specialty
    )


async def test_create_specialty_with_existing_id(
    specialty_repository: MemorySpecialtyRepository, sample_specialty: Specialty
):
    sample_specialty.id = uuid4()
    created_specialty = await specialty_repository.create(sample_specialty)
    assert created_specialty.id == sample_specialty.id
    assert (
        await specialty_repository.get_by_id(created_specialty.id) == created_specialty
    )


async def test_create_specialty_with_none_id(
    specialty_repository: MemorySpecialtyRepository, sample_specialty: Specialty
):
    created_specialty = await specialty_repository.create(sample_specialty)
    assert created_specialty.id is not None
    assert isinstance(created_specialty.id, UUID)
    assert (
        await specialty_repository.get_by_id(created_specialty.id) == created_specialty
    )


async def test_repository_operation_exception_on_create(
    specialty_repository: MemorySpecialtyRepository, sample_specialty: Specialty
):
    specialty_repository.specialties = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await specialty_repository.create(sample_specialty)

    assert "Specialty" in str(exc_info.value)
    assert "create" in str(exc_info.value)
