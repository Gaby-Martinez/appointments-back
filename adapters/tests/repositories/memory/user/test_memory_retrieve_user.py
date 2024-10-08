from dataclasses import replace
from uuid import uuid4

import pytest

from adapters.src.repositories.memory.user_memory_repository import MemoryUserRepository
from core.src.exceptions.repository import RepositoryOperationException
from core.src.models.user import User


async def test_get_by_id(user_repository: MemoryUserRepository, sample_user: User):
    created_user = await user_repository.create(sample_user)
    retrieved_user = await user_repository.get_by_id(created_user.id)

    assert retrieved_user is not None

    assert retrieved_user.ci == sample_user.ci
    assert retrieved_user.password == sample_user.password
    assert retrieved_user.first_name == sample_user.first_name
    assert retrieved_user.last_name == sample_user.last_name
    assert retrieved_user.email == sample_user.email
    assert retrieved_user.date_of_birth == sample_user.date_of_birth
    assert retrieved_user.phone_number == sample_user.phone_number
    assert retrieved_user.document_type == sample_user.document_type
    assert retrieved_user.roles == sample_user.roles
    assert retrieved_user.is_active == sample_user.is_active

    assert retrieved_user.id == created_user.id


async def test_get_by_id_not_found(user_repository: MemoryUserRepository):
    user = await user_repository.get_by_id(uuid4())
    assert user is None


async def test_get_by_id_no_users(user_repository: MemoryUserRepository):
    user = await user_repository.get_by_id(uuid4())
    assert user is None


async def test_inactive_user_retrieval(
    user_repository: MemoryUserRepository, sample_user: User
):
    inactive_user = replace(
        sample_user,
        is_active=False,
        email="inactive@example.com",
        ci="inactive-ci",
    )

    created_inactive_user = await user_repository.create(inactive_user)

    retrieved_user = await user_repository.get_by_id(created_inactive_user.id)
    assert retrieved_user is None

    retrieved_user = await user_repository.get_by_id(
        created_inactive_user.id, include_inactive=True
    )
    assert retrieved_user == created_inactive_user


async def test_get_by_email(user_repository: MemoryUserRepository, sample_user: User):
    created_user = await user_repository.create(sample_user)
    retrieved_user = await user_repository.get_by_email(sample_user.email)
    assert retrieved_user == created_user


async def test_get_by_email_not_found(user_repository: MemoryUserRepository):
    user = await user_repository.get_by_email("nonexistent@example.com")
    assert user is None


async def test_get_users_by_email_no_matching_user(
    user_repository: MemoryUserRepository,
):
    user = await user_repository.get_by_email("not_in_repo@example.com")
    assert user is None


async def test_get_by_ci(user_repository: MemoryUserRepository, sample_user: User):
    created_user = await user_repository.create(sample_user)
    retrieved_user = await user_repository.get_by_ci(sample_user.ci)
    assert retrieved_user == created_user


async def test_get_by_ci_not_found(user_repository: MemoryUserRepository):
    user = await user_repository.get_by_ci("nonexistent-ci")
    assert user is None


async def test_repository_operation_exception_on_get_by_id(
    user_repository: MemoryUserRepository,
):
    user_repository.users = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.get_by_id(uuid4())

    assert "User" in str(exc_info.value)
    assert "get_by_id" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_email(
    user_repository: MemoryUserRepository,
):
    user_repository.email_index = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.get_by_email("test@example.com")

    assert "User" in str(exc_info.value)
    assert "get_by_email" in str(exc_info.value)


async def test_repository_operation_exception_on_get_by_ci(
    user_repository: MemoryUserRepository,
):
    user_repository.ci_index = None  # type: ignore

    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.get_by_ci("1234567890")

    assert "User" in str(exc_info.value)
    assert "get_by_ci" in str(exc_info.value)
