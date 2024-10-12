from typing import List
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.specialty_memory_repository import (
    MemorySpecialtyRepository,
)
from core.src.models import Specialty


@pytest.fixture
async def specialty_repository() -> MemorySpecialtyRepository:
    return MemorySpecialtyRepository()


@pytest.fixture
def sample_specialty_creation():
    return Specialty(
        id=None,
        name="Surgery",
        description="",
        is_active=True,
    )


@pytest.fixture
def sample_specialty():
    return Specialty(
        id=uuid4(),
        name="Internal medicine",
        description="",
        is_active=True,
    )


@pytest.fixture
def inactive_sample_specialty():
    return Specialty(
        id=uuid4(),
        name="Dermathology",
        description="",
        is_active=False,
    )


@pytest.fixture
def specialties() -> List[Specialty]:
    return [
        Specialty(
            id=uuid4(),
            name="Cardiology",
            description="Heart related treatments",
            is_active=True,
        ),
        Specialty(
            id=uuid4(),
            name="Neurology",
            description="Brain and nervous system",
            is_active=True,
        ),
        Specialty(
            id=uuid4(),
            name="Orthopedics",
            description="Musculoskeletal system",
            is_active=True,
        ),
    ]
