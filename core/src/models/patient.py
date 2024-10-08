from dataclasses import dataclass, field
from typing import List

from .role import Role, RoleEnum
from .user import User


@dataclass
class Patient(User):
    roles: List[Role] = field(default_factory=lambda: [Role(name=RoleEnum.PATIENT)])

    def __post_init__(self):
        super().__post_init__()
        if not any(role.name == RoleEnum.PATIENT for role in self.roles):
            raise ValueError("User must have the Patient role")
