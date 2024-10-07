import pytest

from adapters.src.repositories.memory.patient_memory_repository import (
    MemoryPatientRepository,
)
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Patient


async def test_list_include_inactive(
    patient_repository: MemoryPatientRepository,
    sample_patient: Patient,
    inactive_sample_patient: Patient,
) -> None:
    await patient_repository.create(sample_patient)
    await patient_repository.create(inactive_sample_patient)

    active_patients = await patient_repository.list(include_inactive=False)
    assert len(active_patients) == 1
    assert active_patients[0].is_active is True

    all_patients = await patient_repository.list(include_inactive=True)
    assert len(all_patients) == 2


async def test_list_patients(
    patient_repository: MemoryPatientRepository, sample_patient: Patient
) -> None:
    await patient_repository.create(sample_patient)
    patients = await patient_repository.list()
    assert len(patients) == 1
    assert patients[0].id == sample_patient.id


async def test_repository_operation_exception_on_list(
    patient_repository: MemoryPatientRepository,
):
    patient_repository.patients = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await patient_repository.list()

    assert "Patient" in str(exc_info.value)
    assert "list" in str(exc_info.value)
