from dataclasses import dataclass, field
from typing import List, Optional

from .role import Role, RoleEnum
from .specialty import Specialty
from .user import User


@dataclass
class Doctor(User):
    specialty: Optional[Specialty] = None
    roles: List[Role] = field(default_factory=lambda: [Role(name=RoleEnum.DOCTOR)])

    def __post_init__(self):
        super().__post_init__()
        if self.specialty is None:
            raise ValueError("Doctor must have a specialty")
        if not any(role.name == RoleEnum.DOCTOR for role in self.roles):
            raise ValueError("User must have the Doctor role")
