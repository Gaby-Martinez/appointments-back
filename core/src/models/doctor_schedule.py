from datetime import time
from typing import Optional

from pydantic import BaseModel, Field


class DoctorSchedule(BaseModel):
    id: Optional[int] = None
    doctor_id: int
    day_of_week: int = Field(..., ge=1, le=7)
    start_time: time
    end_time: time
    appointment_duration: int = Field(..., gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "doctor_id": 1,
                "day_of_week": 1,
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "appointment_duration": 30,
            }
        }
    }
