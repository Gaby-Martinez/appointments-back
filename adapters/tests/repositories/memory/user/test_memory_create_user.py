from uuid import UUID, uuid4

import pytest

from core.src.exceptions.repository import RepositoryOperationException
from core.src.models.role import Role


async def test_create_user(user_repository, sample_user):
    created_user = await user_repository.create(sample_user)
    assert created_user.id is not None
    assert isinstance(created_user.id, UUID)
    assert await user_repository.get_by_id(created_user.id) == created_user


async def test_create_user_with_existing_id(user_repository, sample_user):
    sample_user.id = uuid4()
    created_user = await user_repository.create(sample_user)
    assert created_user.id == sample_user.id
    assert await user_repository.get_by_id(created_user.id) == created_user


async def test_create_user_with_none_id(user_repository, sample_user):
    sample_user.id = None
    created_user = await user_repository.create(sample_user)
    assert created_user.id is not None
    assert isinstance(created_user.id, UUID)
    assert await user_repository.get_by_id(created_user.id) == created_user


async def test_create_user_with_existing_email(user_repository, sample_user):
    await user_repository.create(sample_user)
    duplicate_user = sample_user.copy()
    duplicate_user.id = None
    duplicate_user.ci = "5610293847"
    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.create(duplicate_user)
    assert "Email already exists" in str(exc_info.value)


async def test_create_user_with_existing_ci(user_repository, sample_user):
    await user_repository.create(sample_user)
    duplicate_user = sample_user.copy()
    duplicate_user.id = None
    duplicate_user.email = "different@email.com"
    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.create(duplicate_user)
    assert "CI already exists" in str(exc_info.value)


async def test_create_user_with_multiple_roles(user_repository, sample_user):
    sample_user.roles = [Role.PATIENT, Role.DOCTOR]
    created_user = await user_repository.create(sample_user)
    assert set(created_user.roles) == {Role.PATIENT, Role.DOCTOR}
    doctors = await user_repository.get_all_doctors()
    patients = await user_repository.get_all_patients()
    assert created_user in doctors and created_user in patients


async def test_repository_operation_exception_on_create(user_repository, sample_user):
    user_repository.users = {}
    user_repository.email_index = {}
    user_repository.ci_index = {}

    user_repository.email_index[sample_user.email] = sample_user.id

    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.create(sample_user)

    assert "User" in str(exc_info.value)
    assert "create" in str(exc_info.value)
