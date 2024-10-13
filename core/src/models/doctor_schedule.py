from dataclasses import dataclass
from datetime import time
from uuid import UUID

from .doctor import Doctor


@dataclass
class DoctorSchedule:
    id: UUID
    doctor: Doctor
    day_of_week: int
    start_time: time
    end_time: time
    appointment_duration: int
    is_active: bool = True
