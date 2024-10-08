from datetime import date
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.user_memory_repository import MemoryUserRepository
from core.src.models import Role, RoleEnum, User


@pytest.fixture
async def user_repository() -> MemoryUserRepository:
    return MemoryUserRepository()


@pytest.fixture
def sample_user_creation():
    return User(
        id=None,
        ci="1234567890",
        password="securepassword123",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        date_of_birth=date(1990, 1, 1),
        phone_number="+1234567890",
        document_type="national_id",
        roles=[Role(name=RoleEnum.PATIENT)],
        is_active=True,
    )


@pytest.fixture
def sample_user():
    return User(
        id=uuid4(),
        ci="1234567890",
        password="securepassword123",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        date_of_birth=date(1990, 1, 1),
        phone_number="+1234567890",
        document_type="national_id",
        roles=[Role(name=RoleEnum.PATIENT)],
        is_active=True,
    )
