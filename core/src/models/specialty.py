from typing import Optional

from pydantic import BaseModel, Field


class Specialty(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Cardiology",
                "description": "Deals with disorders of the heart and blood vessels",
            }
        }
    }
