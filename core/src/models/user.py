from dataclasses import dataclass, field
from datetime import date
from typing import List
from uuid import UUID, uuid4

from core.src.models.role import Role


@dataclass
class User:
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
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if not self.roles:
            raise ValueError("User must have at least one role")

    def is_doctor(self) -> bool:
        return Role.DOCTOR in self.roles

    def is_patient(self) -> bool:
        return Role.PATIENT in self.roles
