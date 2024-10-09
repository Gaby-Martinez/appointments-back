from datetime import date
from typing import List
from uuid import UUID, uuid4

import pytest

from adapters.src.repositories.memory.doctor_memory_repository import (
    MemoryDoctorRepository,
)
from adapters.src.repositories.memory.user_memory_repository import MemoryUserRepository
from core.src.models import Doctor, Role, RoleEnum, Specialty


@pytest.fixture
def doctor_repository(
    user_repository: MemoryUserRepository,
) -> MemoryDoctorRepository:
    return MemoryDoctorRepository(user_repository)


@pytest.fixture
def sample_doctor(sample_specialty: Specialty) -> Doctor:
    return Doctor(
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
        specialty=sample_specialty,
        is_active=True,
    )


@pytest.fixture
def inactive_sample_doctor(sample_specialty: Specialty) -> Doctor:
    return Doctor(
        id=uuid4(),
        email="inactive_doctor@example.com",
        ci="1234567890",
        password="securepassword789",
        first_name="John",
        last_name="Smith",
        date_of_birth=date(1985, 3, 22),
        phone_number="+1234567890",
        document_type="national_id",
        specialty=sample_specialty,
        roles=[Role(name=RoleEnum.DOCTOR)],
        is_active=False,
    )


@pytest.fixture
def doctors_with_mixed_specialties(specialties: List[Specialty]) -> List[Doctor]:
    return [
        Doctor(
            id=UUID("c0a88277-ce8c-4544-a666-4f8f8f3e7608"),
            ci="9876543210",
            password="securepassword456",
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            date_of_birth=date(1990, 5, 15),
            phone_number="+1987654321",
            document_type="national_id",
            roles=[Role(name=RoleEnum.DOCTOR)],
            specialty=specialties[0],  # Cardiology
            is_active=True,
        ),
        Doctor(
            id=UUID("d1b99388-df9d-5655-b777-5f9f9f4e8719"),
            ci="0123456789",
            password="anotherpassword789",
            first_name="John",
            last_name="Smith",
            email="john.smith@example.com",
            date_of_birth=date(1985, 8, 20),
            phone_number="+1123456789",
            document_type="national_id",
            roles=[Role(name=RoleEnum.DOCTOR)],
            specialty=specialties[1],  # Neurology
            is_active=True,
        ),
        Doctor(
            id=UUID("e2c0a499-ef0e-6766-c888-6f0f0f5f9820"),
            ci="9012345678",
            password="thirdpassword101",
            first_name="Alice",
            last_name="Johnson",
            email="alice.johnson@example.com",
            date_of_birth=date(1988, 3, 10),
            phone_number="+1234567890",
            document_type="national_id",
            roles=[Role(name=RoleEnum.DOCTOR)],
            specialty=specialties[0],  # Cardiology
            is_active=True,
        ),
        Doctor(
            id=UUID("f3d1b500-fa1f-7877-d999-7a1a1a6a0931"),
            ci="8901234567",
            password="fourthpassword202",
            first_name="Bob",
            last_name="Williams",
            email="bob.williams@example.com",
            date_of_birth=date(1992, 11, 5),
            phone_number="+1345678901",
            document_type="national_id",
            roles=[Role(name=RoleEnum.DOCTOR)],
            specialty=specialties[2],  # Orthopedics
            is_active=True,
        ),
    ]
