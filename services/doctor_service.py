from typing import List, Optional, Dict
from ..models import Doctor
from .base_service import BaseService
from datetime import date

class DoctorService(BaseService[Doctor]):
    def create_doctor(self,
                     name: str,
                     department_id: int,
                     contact_number: str,
                     email: str,
                     specialization: str,
                     qualifications: List[str],
                     consultation_fee: float) -> Optional[Doctor]:
        staff_id = self._generate_id("STF", "staff")
        doctor_id = self._generate_id("DOC", "doctors")
        
        # First create staff record
        staff_query = """
        INSERT INTO staff (
            staff_id, name, role, department_id, 
            contact_number, email, date_joined
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        staff_params = (
            staff_id, name, "Doctor", department_id,
            contact_number, email, date.today()
        )
        
        if self._execute_query(staff_query, staff_params) is None:
            return None
            
        # Then create doctor record
        doctor_query = """
        INSERT INTO doctors (
            doctor_id, staff_id, specialization,
            qualification, consultation_fee
        ) VALUES (%s, %s, %s, %s, %s)
        """
        doctor_params = (
            doctor_id, staff_id, specialization,
            ','.join(qualifications), consultation_fee
        )
        
        if self._execute_query(doctor_query, doctor_params) is not None:
            return self.get_doctor_by_id(doctor_id)
        return None

    def get_doctor_by_id(self, doctor_id: str) -> Optional[Doctor]:
        query = """
        SELECT d.*, s.name, s.contact_number, s.email, s.department_id,
               s.date_joined
        FROM doctors d
        JOIN staff s ON d.staff_id = s.staff_id
        WHERE d.doctor_id = %s
        """
        result = self._execute_query(query, (doctor_id,))
        return Doctor.from_db_dict(result[0]) if result else None

    def get_available_doctors(self, limit: int = 5) -> List[Doctor]:
        query = """
        SELECT d.*, s.name, s.contact_number, s.email, s.department_id,
               s.date_joined
        FROM doctors d
        JOIN staff s ON d.staff_id = s.staff_id
        WHERE d.is_active = TRUE
        ORDER BY d.doctor_id DESC
        LIMIT %s
        """
        result = self._execute_query(query, (limit,))
        return [Doctor.from_db_dict(row) for row in result] if result else []

    def get_all_doctors(self) -> List[Doctor]:
        query = """
        SELECT d.*, s.name, s.contact_number, s.email, s.department_id,
               s.date_joined
        FROM doctors d
        JOIN staff s ON d.staff_id = s.staff_id
        """
        result = self._execute_query(query)
        return [Doctor.from_db_dict(row) for row in result] if result else []

    def update_doctor(self, doctor: Doctor) -> bool:
        # Update staff information
        staff_query = """
        UPDATE staff 
        SET name = %s, department_id = %s,
            contact_number = %s, email = %s
        WHERE staff_id = %s
        """
        staff_params = (
            doctor.name, doctor.department_id,
            doctor.contact_number, doctor.email,
            doctor.staff_id
        )
        
        if self._execute_query(staff_query, staff_params) is None:
            return False
            
        # Update doctor information
        doctor_query = """
        UPDATE doctors 
        SET specialization = %s, qualification = %s,
            consultation_fee = %s
        WHERE doctor_id = %s
        """
        doctor_params = (
            doctor.specialization,
            ','.join(doctor.qualifications),
            doctor.consultation_fee,
            doctor.doctor_id
        )
        
        return self._execute_query(doctor_query, doctor_params) is not None

    def delete_doctor(self, doctor_id: str) -> bool:
        # Get staff_id first
        query = "SELECT staff_id FROM doctors WHERE doctor_id = %s"
        result = self._execute_query(query, (doctor_id,))
        
        if not result:
            return False
            
        staff_id = result[0]['staff_id']
        
        # Delete doctor record
        doctor_query = "DELETE FROM doctors WHERE doctor_id = %s"
        if self._execute_query(doctor_query, (doctor_id,)) is None:
            return False
            
        # Delete staff record
        staff_query = "DELETE FROM staff WHERE staff_id = %s"
        return self._execute_query(staff_query, (staff_id,)) is not None

    def get_doctor_schedule(self, doctor_id: str, date: date) -> List[Dict]:
        query = """
        SELECT * FROM appointments 
        WHERE doctor_id = %s 
        AND DATE(appointment_date) = %s
        """
        result = self._execute_query(query, (doctor_id, date))
        return result or []
        
    def get_departments(self) -> List[Dict]:
        """Get all departments from the database"""
        query = "SELECT department_id, name FROM departments"
        result = self._execute_query(query)
        return result or []

    def search_doctors(self, search_term: str) -> List[Doctor]:
        query = """
        SELECT d.*, s.name, s.contact_number, s.email, s.department_id
        FROM doctors d
        JOIN staff s ON d.staff_id = s.staff_id
        WHERE s.name LIKE %s 
        OR d.specialization LIKE %s
        """
        search_pattern = f"%{search_term}%"
        params = (search_pattern, search_pattern)
        
        result = self._execute_query(query, params)
        return [Doctor(**row) for row in result] if result else []
