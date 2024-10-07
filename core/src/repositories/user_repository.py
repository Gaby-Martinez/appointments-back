from abc import ABC, abstractmethod
from typing import List, Optional

from core.src.models import Role, User
from core.src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User], ABC):
    @abstractmethod
    async def get_by_email(
        self, email: str, include_inactive: bool = False
    ) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_ci(
        self, ci: str, include_inactive: bool = False
    ) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_users_by_role(
        self, role: Role, include_inactive: bool = False
    ) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_doctors(self, include_inactive: bool = False) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_patients(self, include_inactive: bool = False) -> List[User]:
        raise NotImplementedError
