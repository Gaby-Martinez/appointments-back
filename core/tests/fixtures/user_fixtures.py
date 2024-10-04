from datetime import date

import pytest

from adapters.src.repositories.memory.user_memory_repository import MemoryUserRepository
from core.src.models.role import Role
from core.src.models.user import User


@pytest.fixture
def user_repository():
    return MemoryUserRepository()


@pytest.fixture
def sample_user():
    return User(
        id=None,
        email="test@example.com",
        ci="1234567890",
        password="securepassword123",
        first_name="Test",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        phone_number="+1234567890",
        document_type="national_id",
        roles=[Role.PATIENT],
        is_active=True,
    )
