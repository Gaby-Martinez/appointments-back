from dataclasses import replace
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from core.src.exceptions.repository import RepositoryOperationException
from core.src.models import Appointment
from core.src.repositories.appointment_repository import AppointmentRepository


class MemoryAppointmentRepository(AppointmentRepository):
    def __init__(self) -> None:
        self.appointments: Dict[UUID, Appointment] = {}

    async def create(self, appointment: Appointment) -> Appointment:
        try:
            if appointment.id is None:
                appointment = replace(appointment, id=uuid4())
            self.appointments[appointment.id] = appointment
            return appointment
        except Exception as e:
            raise RepositoryOperationException("Appointment", "create", str(e))

    async def get_by_id(
        self, appointment_id: UUID, include_inactive: bool = False
    ) -> Optional[Appointment]:
        try:
            return self.appointments.get(appointment_id)
        except Exception as e:
            raise RepositoryOperationException("Appointment", "get_by_id", str(e))

    async def list(self, include_inactive: bool = False) -> List[Appointment]:
        try:
            return list(self.appointments.values())
        except Exception as e:
            raise RepositoryOperationException("Appointment", "list", str(e))

    async def get_by_doctor_id(self, doctor_id: UUID) -> List[Appointment]:
        try:
            return [
                appointment
                for appointment in self.appointments.values()
                if appointment.doctor.id == doctor_id
            ]
        except Exception as e:
            raise RepositoryOperationException(
                "Appointment", "get_by_doctor_id", str(e)
            )

    async def get_by_patient_id(self, patient_id: UUID) -> List[Appointment]:
        try:
            return [
                appointment
                for appointment in self.appointments.values()
                if appointment.patient.id == patient_id
            ]
        except Exception as e:
            raise RepositoryOperationException(
                "Appointment", "get_by_patient_id", str(e)
            )

    async def get_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Appointment]:
        try:
            return [
                appointment
                for appointment in self.appointments.values()
                if start_date <= appointment.start_datetime < end_date
            ]
        except Exception as e:
            raise RepositoryOperationException(
                "Appointment", "get_by_date_range", str(e)
            )

    async def get_by_doctor_and_time_range(
        self, doctor_id: UUID, start_time: datetime, end_time: datetime
    ) -> List[Appointment]:
        try:
            return [
                appointment
                for appointment in self.appointments.values()
                if appointment.doctor.id == doctor_id
                and appointment.start_datetime < end_time
                and (
                    appointment.start_datetime + timedelta(minutes=appointment.duration)
                )
                > start_time
            ]
        except Exception as e:
            raise RepositoryOperationException(
                "Appointment", "get_by_doctor_and_time_range", str(e)
            )
