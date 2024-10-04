import pytest

from core.src.exceptions.repository import RepositoryOperationException
from core.src.models.role import Role


async def test_list_users(user_repository, sample_user):
    created_user = await user_repository.create(sample_user)
    users_list = await user_repository.list()
    assert len(users_list) == 1
    assert users_list[0] == created_user


async def test_list_users_with_inactive(user_repository, sample_user):
    active_user = await user_repository.create(sample_user)

    inactive_user = sample_user.model_copy(
        update={
            "id": None,
            "is_active": False,
            "email": "inactive@example.com",
            "ci": "inactive-ci",
        }
    )
    await user_repository.create(inactive_user)

    active_users = await user_repository.list(include_inactive=False)

    all_users = await user_repository.list(include_inactive=True)

    assert len(active_users) == 1
    assert active_user in active_users
    assert inactive_user not in active_users

    assert len(all_users) == 2
    assert active_user in all_users
    assert inactive_user in all_users


async def test_list_excludes_inactive_users(user_repository, sample_user):
    inactive_user = sample_user.model_copy(
        update={
            "id": None,
            "is_active": False,
            "email": "inactive@example.com",
            "ci": "inactive-ci",
        }
    )
    await user_repository.create(inactive_user)

    active_users = await user_repository.list(include_inactive=False)
    assert len(active_users) == 0


async def test_list_with_active_and_inactive_users(user_repository, sample_user):
    users = [
        sample_user,
        sample_user.model_copy(
            update={"email": "user2@example.com", "ci": "ci2", "roles": [Role.DOCTOR]}
        ),
        sample_user.model_copy(
            update={"email": "user3@example.com", "ci": "ci3", "is_active": False}
        ),
    ]

    for user in users:
        user.id = None
        await user_repository.create(user)

    all_users = await user_repository.list(include_inactive=True)
    active_users = await user_repository.list(include_inactive=False)
    doctors = await user_repository.get_all_doctors()
    patients = await user_repository.get_all_patients()

    assert len(all_users) == 3
    assert len(active_users) == 2
    assert len(doctors) == 1
    assert len(patients) == 1


async def test_get_users_by_role(user_repository, sample_user):
    _patient_user = await user_repository.create(sample_user)

    doctor_user = sample_user.model_copy(
        update={
            "id": None,
            "roles": [Role.DOCTOR],
            "email": "doctor@example.com",
            "ci": "987654321",
        }
    )
    await user_repository.create(doctor_user)

    doctors = await user_repository.get_users_by_role(Role.DOCTOR)
    patients = await user_repository.get_users_by_role(Role.PATIENT)

    assert len(doctors) == 1
    assert doctors[0].email == "doctor@example.com"
    assert len(patients) == 1
    assert patients[0].email == "test@example.com"


async def test_get_all_doctors(user_repository, sample_user):
    await user_repository.create(sample_user)  # Patient

    doctor_user = sample_user.model_copy(
        update={
            "id": None,
            "roles": [Role.DOCTOR],
            "email": "doctor@example.com",
            "ci": "doctor-ci",
        }
    )
    await user_repository.create(doctor_user)

    doctors = await user_repository.get_all_doctors()

    assert len(doctors) == 1
    assert doctors[0].email == "doctor@example.com"


async def test_get_all_patients(user_repository, sample_user):
    await user_repository.create(sample_user)  # Patient

    doctor_user = sample_user.model_copy(
        update={
            "id": None,
            "roles": [Role.DOCTOR],
            "email": "doctor@example.com",
            "ci": "doctor-ci",
        }
    )
    await user_repository.create(doctor_user)

    patients = await user_repository.get_all_patients()

    assert len(patients) == 1
    assert patients[0].email == "test@example.com"


async def test_list_no_matching_role(user_repository):
    doctors = await user_repository.get_users_by_role(Role.DOCTOR)
    assert doctors == []


async def test_get_all_patients_no_users(user_repository):
    patients = await user_repository.get_all_patients()
    assert patients == []


async def test_repository_operation_exception_on_list(user_repository):
    user_repository.users = None

    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.list()

    assert "User" in str(exc_info.value)
    assert "list" in str(exc_info.value)


async def test_repository_operation_exception_on_get_users_by_role(user_repository):
    user_repository.users = None

    with pytest.raises(RepositoryOperationException) as exc_info:
        await user_repository.get_users_by_role(Role.DOCTOR)

    assert "User" in str(exc_info.value)
    assert "get_users_by_role" in str(exc_info.value)
