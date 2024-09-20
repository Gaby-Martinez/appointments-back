from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from core.src.models.role import Role


class User(BaseModel):
    id: Optional[int] = None
    ci: str = Field(..., min_length=5, max_length=20)
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    date_of_birth: date
    phone_number: str = Field(..., pattern=r"^\+?1?\d{9,15}$")
    document_type: str = Field(..., max_length=20)
    roles: List[Role] = Field(..., min_length=1)

    def is_doctor(self) -> bool:
        return Role.DOCTOR in self.roles

    def is_patient(self) -> bool:
        return Role.PATIENT in self.roles

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ci": "1234567890",
                "password": "securepassword",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "date_of_birth": "1990-01-01",
                "phone_number": "+1234567890",
                "document_type": "national_id",
                "roles": [Role.PATIENT],
            }
        }
    )
