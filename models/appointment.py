from typing import Dict, Optional
from datetime import datetime

class Appointment:
    def __init__(
        self,
        appointment_id: str,
        patient_id: str,
        doctor_id: str,
        date_time: datetime,
        department: str,
        status: str = 'scheduled',
        notes: Optional[str] = None
    ):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_time = date_time
        self.department = department
        self.status = status
        self.notes = notes

    @staticmethod
    def from_db_dict(data: Dict) -> 'Appointment':
        return Appointment(
            appointment_id=data['appointment_id'],
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            date_time=data['appointment_date'],
            department=data.get('department', ''),
            status=data['status'],
            notes=data.get('notes')
        )

    def to_dict(self) -> Dict:
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_date': self.date_time,
            'department': self.department,
            'status': self.status,
            'notes': self.notes
        }

    def reschedule(self, new_date_time: datetime):
        self.date_time = new_date_time
        self.status = 'rescheduled'

    def cancel(self):
        self.status = 'cancelled'

    def complete(self):
        self.status = 'completed'

    def add_notes(self, notes: str):
        self.notes = notes
