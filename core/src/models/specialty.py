from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Specialty:
    id: UUID
    name: str
    description: Optional[str] = None
    is_active: bool = True
