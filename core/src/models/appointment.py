from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .appointment_status import AppointmentStatus
from .doctor import Doctor
from .patient import Patient


@dataclass
class Appointment:
    id: UUID
    doctor: Doctor
    patient: Patient
    start_datetime: datetime
    duration: int
    status: AppointmentStatus
