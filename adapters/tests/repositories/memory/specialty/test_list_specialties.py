from dataclasses import replace
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.specialty_memory_repository import (
    MemorySpecialtyRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Specialty


async def test_list_specialties(
    specialty_repository: MemorySpecialtyRepository, sample_specialty: Specialty
):
    created_specialty = await specialty_repository.create(sample_specialty)
    specialties_list = await specialty_repository.list()
    assert len(specialties_list) == 1
    assert specialties_list[0] == created_specialty


async def test_list_specialties_with_inactive(
    specialty_repository: MemorySpecialtyRepository, sample_specialty: Specialty
):
    active_specialty = await specialty_repository.create(sample_specialty)
    inactive_specialty = replace(sample_specialty, id=uuid4(), is_active=False)
    await specialty_repository.create(inactive_specialty)

    active_specialties = await specialty_repository.list(include_inactive=False)

    all_specialties = await specialty_repository.list(include_inactive=True)

    assert len(active_specialties) == 1
    assert active_specialty in active_specialties
    assert inactive_specialty not in active_specialties

    assert len(all_specialties) == 2
    assert active_specialty in all_specialties
    assert inactive_specialty in all_specialties


async def test_list_excludes_inactive_specialties(
    specialty_repository: MemorySpecialtyRepository, sample_specialty: Specialty
):
    inactive_specialty = replace(
        sample_specialty,
        id=uuid4(),
        is_active=False,
    )

    await specialty_repository.create(inactive_specialty)

    active_specialties = await specialty_repository.list(include_inactive=False)
    assert len(active_specialties) == 0


async def test_list_with_active_and_inactive_specialties(
    specialty_repository: MemorySpecialtyRepository, sample_specialty: Specialty
):
    specialties = [
        sample_specialty,
        replace(
            sample_specialty,
            id=uuid4(),
            name="Psychiatry",
        ),
        replace(
            sample_specialty,
            id=uuid4(),
            name="Pediatrics",
            is_active=False,
        ),
    ]

    for specialty in specialties:
        await specialty_repository.create(specialty)

    all_specialties = await specialty_repository.list(include_inactive=True)
    active_specialties = await specialty_repository.list(include_inactive=False)

    assert len(all_specialties) == 3
    assert len(active_specialties) == 2


async def test_list_no_specialties(specialty_repository: MemorySpecialtyRepository):
    specialties = await specialty_repository.list()
    assert specialties == []


async def test_repository_operation_exception_on_list(
    specialty_repository: MemorySpecialtyRepository,
):
    specialty_repository.specialties = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await specialty_repository.list()

    assert "Specialty" in str(exc_info.value)
    assert "list" in str(exc_info.value)
