from dataclasses import dataclass, field
from datetime import date
from typing import List
from uuid import UUID

from core.src.models.role import Role, RoleEnum


@dataclass
class User:
    id: UUID
    ci: str
    password: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: date
    phone_number: str
    document_type: str
    roles: List[Role] = field(default_factory=list)
    is_active: bool = True

    def __post_init__(self):
        if not self.roles:
            raise ValueError("User must have at least one role")

    def is_doctor(self) -> bool:
        return any(role.name == RoleEnum.DOCTOR for role in self.roles)

    def is_patient(self) -> bool:
        return any(role.name == RoleEnum.PATIENT for role in self.roles)
