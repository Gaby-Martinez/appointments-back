from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AppointmentStatusEnum(Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


@dataclass
class AppointmentStatus:
    name: AppointmentStatusEnum
    id: Optional[int] = None
