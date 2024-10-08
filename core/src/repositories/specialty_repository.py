from abc import ABC

from core.src.models import Specialty

from .base_repository import BaseRepository


class SpecialtyRepository(BaseRepository[Specialty], ABC):
    pass
