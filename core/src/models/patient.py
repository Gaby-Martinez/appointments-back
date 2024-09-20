from typing import Optional

from pydantic import BaseModel


class Patient(BaseModel):
    id: Optional[int] = None
    user_id: int

    model_config = {"json_schema_extra": {"example": {"id": 1, "user_id": 1}}}
