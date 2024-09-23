from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field


class Appointment(BaseModel):
    id: Optional[int] = None
    patient_id: int
    doctor_id: int
    appointment_date: date
    start_time: time
    duration: int = Field(..., gt=0)
    status: str = Field(..., max_length=20)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "patient_id": 1,
                "doctor_id": 1,
                "appointment_date": "2023-06-15",
                "start_time": "14:30:00",
                "duration": 30,
                "status": "scheduled",
            }
        }
    }
