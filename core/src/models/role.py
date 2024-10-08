from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RoleEnum(Enum):
    DOCTOR = "Doctor"
    PATIENT = "Patient"


@dataclass
class Role:
    name: RoleEnum
    id: Optional[int] = None
