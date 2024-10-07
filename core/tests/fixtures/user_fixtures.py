from datetime import date

import pytest

from adapters.src.repositories.memory.user_memory_repository import MemoryUserRepository
from core.src.models import Role, User


@pytest.fixture
def user_repository():
    return MemoryUserRepository()


@pytest.fixture
def sample_user():
    return User(
        ci="1234567890",
        password="securepassword123",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        date_of_birth=date(1990, 1, 1),
        phone_number="+1234567890",
        document_type="national_id",
        roles=[Role.PATIENT],
        is_active=True,
    )
