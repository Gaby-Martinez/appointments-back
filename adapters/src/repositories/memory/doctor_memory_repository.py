from typing import Dict, List, Optional
from uuid import UUID

from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Doctor
from core.src.repositories.doctor_repository import DoctorRepository
from core.src.repositories.user_repository import UserRepository


class MemoryDoctorRepository(DoctorRepository):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.doctors: Dict[UUID, Doctor] = {}

    async def create(self, doctor: Doctor) -> Doctor:
        try:
            created_user = await self.user_repository.create(doctor)
            doctor_with_details = Doctor(
                ci=created_user.ci,
                password=created_user.password,
                first_name=created_user.first_name,
                last_name=created_user.last_name,
                email=created_user.email,
                date_of_birth=created_user.date_of_birth,
                phone_number=created_user.phone_number,
                document_type=created_user.document_type,
                roles=created_user.roles,
                is_active=created_user.is_active,
                id=created_user.id,
                specialty=doctor.specialty,
            )

            self.doctors[created_user.id] = doctor_with_details
            return doctor_with_details
        except Exception as e:
            raise RepositoryOperationException("Doctor", "create", str(e))

    async def get_by_id(
        self, doctor_id: UUID, include_inactive: bool = False
    ) -> Optional[Doctor]:
        try:
            doctor = self.doctors.get(doctor_id)
            if doctor and (include_inactive or doctor.is_active):
                return doctor
            return None
        except Exception as e:
            raise RepositoryOperationException("Doctor", "get_by_id", str(e))

    async def list(self, include_inactive: bool = False) -> List[Doctor]:
        try:
            if include_inactive:
                return list(self.doctors.values())
            return [doctor for doctor in self.doctors.values() if doctor.is_active]
        except Exception as e:
            raise RepositoryOperationException("Doctor", "list", str(e))

    async def get_by_email(
        self, email: str, include_inactive: bool = False
    ) -> Optional[Doctor]:
        try:
            user = await self.user_repository.get_by_email(email, include_inactive)
            if user:
                return self.doctors.get(user.id)
            return None
        except Exception as e:
            raise RepositoryOperationException("Doctor", "get_by_email", str(e))

    async def get_by_ci(
        self, ci: str, include_inactive: bool = False
    ) -> Optional[Doctor]:
        try:
            user = await self.user_repository.get_by_ci(ci, include_inactive)
            if user:
                return self.doctors.get(user.id)
            return None
        except Exception as e:
            raise RepositoryOperationException("Doctor", "get_by_ci", str(e))

    async def get_doctors_by_specialty(self, specialty_id: UUID) -> List[Doctor]:
        try:
            return [
                doctor
                for doctor in self.doctors.values()
                if doctor.specialty is not None and doctor.specialty.id == specialty_id
            ]
        except Exception as e:
            raise RepositoryOperationException("Doctor", "get_by_specialty", str(e))
