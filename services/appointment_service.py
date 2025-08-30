from typing import List, Optional, Dict
from datetime import datetime
from ..models import Appointment
from ..patterns.observer import AppointmentSystem
from ..auth.rbac import AuthenticationManager, Permission, require_permission, require_self_or_admin
from .base_service import BaseService

class AppointmentService(BaseService[Appointment]):
    def __init__(self):
        super().__init__()
        self.notification_system = AppointmentSystem()

    @require_permission(Permission.CREATE_APPOINTMENT)
    @require_self_or_admin(resource_id_param="patient_id")
    def create_appointment(self,
                         patient_id: str,
                         doctor_id: str,
                         date_time: datetime,
                         department: str,
                         notes: str = None) -> Optional[Appointment]:
        appointment_id = self._generate_id("APT", "appointments")
        
        query = """
        INSERT INTO appointments (
            appointment_id, patient_id, doctor_id,
            appointment_date, department, status, notes
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            appointment_id, patient_id, doctor_id,
            date_time, department, 'scheduled', notes
        )
        
        if self._execute_query(query, params) is not None:
            # Get patient and doctor details for notification
            patient_data = self._get_patient_data(patient_id)
            doctor_data = self._get_doctor_data(doctor_id)
            
            # Notify observers
            self.notification_system.schedule_appointment(
                patient_data,
                doctor_data,
                date_time
            )
            
            return self.get_appointment_by_id(appointment_id)
        return None

    def get_appointment_by_id(self, appointment_id: str) -> Optional[Appointment]:
        query = """
        SELECT * FROM appointments WHERE appointment_id = %s
        """
        result = self._execute_query(query, (appointment_id,))
        return Appointment(**result[0]) if result else None
        
    @require_permission(Permission.VIEW_APPOINTMENTS)
    def get_appointments(self, start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None,
                        status: Optional[str] = None,
                        search_term: Optional[str] = None) -> List[Appointment]:
        query = """
        SELECT a.*, p.name as patient_name, d.name as doctor_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors doc ON a.doctor_id = doc.doctor_id
        JOIN staff d ON doc.staff_id = d.staff_id
        WHERE 1=1
        """
        params = []

        if start_date and end_date:
            query += " AND DATE(appointment_date) BETWEEN %s AND %s"
            params.extend([start_date, end_date])

        if status:
            query += " AND status = %s"
            params.append(status)

        if search_term:
            query += " AND (p.name LIKE %s OR d.name LIKE %s)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern])

        query += " ORDER BY appointment_date DESC"
        result = self._execute_query(query, tuple(params) if params else None)
        return [Appointment(**row) for row in result] if result else []
        
    def get_appointments_by_date(self, date: datetime) -> List[Appointment]:
        query = """
        SELECT * FROM appointments 
        WHERE DATE(appointment_date) = DATE(%s)
        """
        result = self._execute_query(query, (date,))
        return [Appointment(**row) for row in result] if result else []

    def get_recent_appointments(self, limit: int = 5) -> List[Appointment]:
        query = """
        SELECT * FROM appointments 
        ORDER BY appointment_date DESC 
        LIMIT %s
        """
        result = self._execute_query(query, (limit,))
        return [Appointment(**row) for row in result] if result else []
        
        if result and len(result) > 0:
            return Appointment.from_db_dict(result[0])
        return None

    def get_appointments_by_patient(self, patient_id: str) -> List[Appointment]:
        query = """
        SELECT a.*, d.name as doctor_name
        FROM appointments a
        JOIN doctors doc ON a.doctor_id = doc.doctor_id
        JOIN staff d ON doc.staff_id = d.staff_id
        WHERE a.patient_id = %s
        ORDER BY a.appointment_date DESC
        """
        result = self._execute_query(query, (patient_id,))
        return [Appointment.from_db_dict(row) for row in (result or [])]

    def get_appointments_by_doctor(self, doctor_id: str) -> List[Appointment]:
        query = """
        SELECT a.*, p.name as patient_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        WHERE a.doctor_id = %s
        ORDER BY a.appointment_date DESC
        """
        result = self._execute_query(query, (doctor_id,))
        return [Appointment.from_db_dict(row) for row in (result or [])]

    def update_appointment_status(self, 
                                appointment_id: str, 
                                status: str,
                                notes: str = None) -> bool:
        query = """
        UPDATE appointments 
        SET status = %s, notes = COALESCE(%s, notes)
        WHERE appointment_id = %s
        """
        return self._execute_query(query, (status, notes, appointment_id)) is not None

    def reschedule_appointment(self,
                             appointment_id: str,
                             new_date_time: datetime) -> bool:
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            return False
            
        query = """
        UPDATE appointments 
        SET appointment_date = %s, status = 'rescheduled'
        WHERE appointment_id = %s
        """
        success = self._execute_query(query, (new_date_time, appointment_id)) is not None
        
        if success:
            # Get patient and doctor details for notification
            patient_data = self._get_patient_data(appointment.patient_id)
            doctor_data = self._get_doctor_data(appointment.doctor_id)
            
            # Notify observers
            self.notification_system.notify(
                "APPOINTMENT_RESCHEDULED",
                {
                    "appointment_id": appointment_id,
                    "patient": patient_data,
                    "doctor": doctor_data,
                    "new_date_time": new_date_time
                }
            )
        
        return success

    def cancel_appointment(self, appointment_id: str, reason: str = None) -> bool:
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            return False
            
        success = self.update_appointment_status(appointment_id, 'cancelled', reason)
        
        if success:
            self.notification_system.cancel_appointment(appointment_id, reason)
        
        return success

    def _get_patient_data(self, patient_id: str) -> Dict:
        query = "SELECT * FROM patients WHERE patient_id = %s"
        result = self._execute_query(query, (patient_id,))
        return result[0] if result else {}

    def _get_doctor_data(self, doctor_id: str) -> Dict:
        query = """
        SELECT d.*, s.name, s.email, s.contact_number
        FROM doctors d
        JOIN staff s ON d.staff_id = s.staff_id
        WHERE d.doctor_id = %s
        """
        result = self._execute_query(query, (doctor_id,))
        return result[0] if result else {}
