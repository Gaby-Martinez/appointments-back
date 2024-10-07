from typing import Dict, List, Optional
from uuid import UUID

from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Patient
from core.src.repositories.patient_repository import PatientRepository
from core.src.repositories.user_repository import UserRepository


class MemoryPatientRepository(PatientRepository):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.patients: Dict[UUID, Patient] = {}

    async def create(self, patient: Patient) -> Patient:
        try:
            created_user = await self.user_repository.create(patient)
            patient_with_details = Patient(
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
            )

            self.patients[created_user.id] = patient_with_details
            return patient_with_details
        except Exception as e:
            raise RepositoryOperationException("Patient", "create", str(e))

    async def get_by_id(
        self, patient_id: UUID, include_inactive: bool = False
    ) -> Optional[Patient]:
        try:
            patient = self.patients.get(patient_id)
            if patient and (include_inactive or patient.is_active):
                return patient
            return None
        except Exception as e:
            raise RepositoryOperationException("Patient", "get_by_id", str(e))

    async def list(self, include_inactive: bool = False) -> List[Patient]:
        try:
            if include_inactive:
                return list(self.patients.values())
            return [patient for patient in self.patients.values() if patient.is_active]
        except Exception as e:
            raise RepositoryOperationException("Patient", "list", str(e))

    async def get_by_email(
        self, email: str, include_inactive: bool = False
    ) -> Optional[Patient]:
        try:
            user = await self.user_repository.get_by_email(email, include_inactive)
            if user:
                return self.patients.get(user.id)
            return None
        except Exception as e:
            raise RepositoryOperationException("Patient", "get_by_email", str(e))

    async def get_by_ci(
        self, ci: str, include_inactive: bool = False
    ) -> Optional[Patient]:
        try:
            user = await self.user_repository.get_by_ci(ci, include_inactive)
            if user:
                return self.patients.get(user.id)
            return None
        except Exception as e:
            raise RepositoryOperationException("Patient", "get_by_ci", str(e))
