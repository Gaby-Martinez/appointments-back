from typing import List
from uuid import UUID

import pytest

from adapters.src.repositories.memory.doctor_memory_repository import (
    MemoryDoctorRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Doctor, Specialty


async def test_list_doctors(
    doctor_repository: MemoryDoctorRepository, sample_doctor: Doctor
) -> None:
    await doctor_repository.create(sample_doctor)
    doctors = await doctor_repository.list()
    assert len(doctors) == 1
    assert doctors[0].id == sample_doctor.id


async def test_get_doctors_by_specialty(
    doctor_repository: MemoryDoctorRepository,
    doctors_with_mixed_specialties: List[Doctor],
    specialties: List[Specialty],
) -> None:
    for doctor in doctors_with_mixed_specialties:
        await doctor_repository.create(doctor)

    for specialty in specialties:
        retrieved_doctors = await doctor_repository.get_doctors_by_specialty(
            specialty.id
        )

        expected_doctors = [
            d
            for d in doctors_with_mixed_specialties
            if d.specialty is not None and d.specialty.id == specialty.id
        ]

        assert retrieved_doctors is not None
        assert len(retrieved_doctors) == len(expected_doctors)

        retrieved_ids = {doctor.id for doctor in retrieved_doctors}
        expected_ids = {doctor.id for doctor in expected_doctors}
        assert retrieved_ids == expected_ids, f"Mismatch for specialty {specialty.name}"

        for doctor in retrieved_doctors:
            assert (
                doctor.specialty is not None
            ), f"Retrieved doctor has no specialty for {specialty.name} query"
            assert (
                doctor.specialty.id == specialty.id
            ), f"Wrong specialty for doctor in {specialty.name} query"

    non_existent_specialty_id = UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")
    empty_result = await doctor_repository.get_doctors_by_specialty(
        non_existent_specialty_id
    )
    assert (
        len(empty_result) == 0
    ), "Query with non-existent specialty should return empty list"


async def test_list_include_inactive(
    doctor_repository: MemoryDoctorRepository,
    sample_doctor: Doctor,
    inactive_sample_doctor: Doctor,
) -> None:
    await doctor_repository.create(sample_doctor)
    await doctor_repository.create(inactive_sample_doctor)

    active_doctors = await doctor_repository.list(include_inactive=False)
    assert len(active_doctors) == 1
    assert active_doctors[0].is_active is True

    all_doctors = await doctor_repository.list(include_inactive=True)
    assert len(all_doctors) == 2


async def test_repository_operation_exception_on_list(
    doctor_repository: MemoryDoctorRepository,
):
    doctor_repository.doctors = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await doctor_repository.list()

    assert "Doctor" in str(exc_info.value)
    assert "list" in str(exc_info.value)
