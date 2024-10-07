from dataclasses import replace
from datetime import date
from uuid import UUID, uuid4

import pytest

from adapters.src.repositories.memory.user_memory_repository import MemoryUserRepository
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Role, User


async def test_create_user(user_repository: MemoryUserRepository, sample_user: User):
    created_user = await user_repository.create(sample_user)
    assert created_user.id is not None
    assert isinstance(created_user.id, UUID)
    assert await user_repository.get_by_id(created_user.id) == created_user


async def test_create_user_with_no_roles(user_repository: MemoryUserRepository) -> None:
    with pytest.raises(ValueError, match="User must have at least one role"):
        invalid_user = User(
            ci="000000000",
            password="securepassword123",
            first_name="Test",
            last_name="User",
            email="no_role_user@example.com",
            date_of_birth=date(1990, 1, 1),
            phone_number="+1234567890",
            document_type="national_id",
            roles=[],  # No roles
            is_active=True,
        )
        await user_repository.create(invalid_user)


async def test_create_user_with_existing_id(
    user_repository: MemoryUserRepository, sample_user: User
):
    sample_user.id = uuid4()
    created_user = await user_repository.create(sample_user)
    assert created_user.id == sample_user.id
    assert await user_repository.get_by_id(created_user.id) == created_user


async def test_create_user_with_none_id(
    user_repository: MemoryUserRepository, sample_user: User
):
    created_user = await user_repository.create(sample_user)
    assert created_user.id is not None
    assert isinstance(created_user.id, UUID)
    assert await user_repository.get_by_id(created_user.id) == created_user


async def test_create_user_with_existing_email(
    user_repository: MemoryUserRepository, sample_user: User
):
    await user_repository.create(sample_user)
    duplicate_user = replace(sample_user, ci="5610293847")
    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.create(duplicate_user)
    assert "Email already exists" in str(exc_info.value)


async def test_create_user_with_existing_ci(
    user_repository: MemoryUserRepository, sample_user: User
):
    await user_repository.create(sample_user)
    duplicate_user = replace(sample_user, email="different@email.com")
    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.create(duplicate_user)
    assert "CI already exists" in str(exc_info.value)


async def test_create_user_with_multiple_roles(
    user_repository: MemoryUserRepository, sample_user: User
):
    sample_user.roles = [Role.PATIENT, Role.DOCTOR]
    created_user = await user_repository.create(sample_user)
    assert set(created_user.roles) == {Role.PATIENT, Role.DOCTOR}
    doctors = await user_repository.get_all_doctors()
    patients = await user_repository.get_all_patients()
    assert created_user in doctors and created_user in patients


async def test_repository_operation_exception_on_create(
    user_repository: MemoryUserRepository, sample_user: User
):
    user_repository.users = {}
    user_repository.email_index = {}
    user_repository.ci_index = {}

    user_repository.email_index[sample_user.email] = sample_user.id

    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.create(sample_user)

    assert "User" in str(exc_info.value)
    assert "create" in str(exc_info.value)
