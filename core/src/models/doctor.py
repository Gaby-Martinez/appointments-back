from typing import Optional

from pydantic import BaseModel


class Doctor(BaseModel):
    id: Optional[int] = None
    user_id: int
    specialty_id: int

    model_config = {
        "json_schema_extra": {"example": {"id": 1, "user_id": 2, "specialty_id": 1}}
    }
