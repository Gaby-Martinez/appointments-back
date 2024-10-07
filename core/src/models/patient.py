from dataclasses import dataclass, field
from typing import List

from .role import Role
from .user import User


@dataclass
class Patient(User):
    roles: List[Role] = field(default_factory=lambda: [Role.PATIENT])

    def __post_init__(self):
        super().__post_init__()
        if Role.PATIENT not in self.roles:
            raise ValueError("Must have patient role")
