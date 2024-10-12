from dataclasses import replace
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.specialty_memory_repository import (
    MemorySpecialtyRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Specialty


async def test_get_by_id(
    specialty_repository: MemorySpecialtyRepository, sample_specialty: Specialty
):
    created_specialty = await specialty_repository.create(sample_specialty)
    retrieved_specialty = await specialty_repository.get_by_id(created_specialty.id)

    assert retrieved_specialty is not None

    assert retrieved_specialty.name == sample_specialty.name
    assert retrieved_specialty.description == sample_specialty.description
    assert retrieved_specialty.is_active == sample_specialty.is_active

    assert retrieved_specialty.id == created_specialty.id


async def test_get_by_id_not_found(specialty_repository: MemorySpecialtyRepository):
    specialty = await specialty_repository.get_by_id(uuid4())
    assert specialty is None


async def test_get_by_id_no_specialties(
    specialty_repository: MemorySpecialtyRepository,
):
    specialty = await specialty_repository.get_by_id(uuid4())
    assert specialty is None


async def test_inactive_specialty_retrieval(
    specialty_repository: MemorySpecialtyRepository, sample_specialty: Specialty
):
    inactive_specialty = replace(
        sample_specialty,
        is_active=False,
    )

    created_inactive_specialty = await specialty_repository.create(inactive_specialty)

    retrieved_specialty = await specialty_repository.get_by_id(
        created_inactive_specialty.id
    )
    assert retrieved_specialty is None

    retrieved_specialty = await specialty_repository.get_by_id(
        created_inactive_specialty.id, include_inactive=True
    )
    assert retrieved_specialty == created_inactive_specialty


async def test_repository_operation_exception_on_get_by_id(
    specialty_repository: MemorySpecialtyRepository,
):
    specialty_repository.specialties = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await specialty_repository.get_by_id(uuid4())

    assert "Specialty" in str(exc_info.value)
    assert "get_by_id" in str(exc_info.value)
