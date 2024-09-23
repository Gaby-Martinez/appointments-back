from abc import ABC, abstractmethod
from typing import Optional

from core.src.models.user import User
from core.src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User], ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_ci(self, ci: str) -> Optional[User]:
        pass
