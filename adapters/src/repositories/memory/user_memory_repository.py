from typing import List, Optional
from uuid import UUID, uuid4

from core.src.exceptions.repository import RepositoryOperationException
from core.src.models.role import Role
from core.src.models.user import User
from core.src.repositories.user_repository import UserRepository


class MemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.email_index = {}
        self.ci_index = {}

    async def create(self, user: User) -> User:
        try:
            if user.id is None:
                user.id = uuid4()

            self.users[user.id] = user
            self.email_index[user.email] = user.id
            self.ci_index[user.ci] = user.id
            return user
        except Exception as e:
            if self.users is not None:
                self.users.pop(user.id, None)
            if self.email_index is not None:
                self.email_index.pop(user.email, None)
            if self.ci_index is not None:
                self.ci_index.pop(user.ci, None)
            raise RepositoryOperationException("User", "create", str(e))

    async def get_by_id(
        self, user_id: UUID, include_inactive: bool = False
    ) -> Optional[User]:
        try:
            user = self.users.get(user_id)
            if user and (include_inactive or user.is_active):
                return user
            return None
        except Exception as e:
            raise RepositoryOperationException("User", "get_by_id", str(e))

    async def get_by_email(
        self, email: str, include_inactive: bool = False
    ) -> Optional[User]:
        try:
            user_id = self.email_index.get(email)
            if user_id:
                user = self.users.get(user_id)
                if user and (include_inactive or user.is_active):
                    return user
            return None
        except Exception as e:
            raise RepositoryOperationException("User", "get_by_email", str(e))

    async def get_by_ci(
        self, ci: str, include_inactive: bool = False
    ) -> Optional[User]:
        try:
            user_id = self.ci_index.get(ci)
            if user_id:
                user = self.users.get(user_id)
                if user and (include_inactive or user.is_active):
                    return user
            return None
        except Exception as e:
            raise RepositoryOperationException("User", "get_by_ci", str(e))

    async def list(self, include_inactive: bool = False) -> List[User]:
        try:
            if include_inactive:
                return list(self.users.values())
            return [user for user in self.users.values() if user.is_active]
        except Exception as e:
            raise RepositoryOperationException("User", "list", str(e))

    async def get_users_by_role(
        self, role: Role, include_inactive: bool = False
    ) -> List[User]:
        try:
            return [
                user
                for user in self.users.values()
                if role in user.roles and (include_inactive or user.is_active)
            ]
        except Exception as e:
            raise RepositoryOperationException("User", "get_users_by_role", str(e))

    async def get_all_doctors(self, include_inactive: bool = False) -> List[User]:
        try:
            return await self.get_users_by_role(Role.DOCTOR, include_inactive)
        except Exception as e:
            raise RepositoryOperationException("User", "get_all_doctors", str(e))

    async def get_all_patients(self, include_inactive: bool = False) -> List[User]:
        try:
            return await self.get_users_by_role(Role.PATIENT, include_inactive)
        except Exception as e:
            raise RepositoryOperationException("User", "get_all_patients", str(e))
