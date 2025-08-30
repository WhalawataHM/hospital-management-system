from typing import List, Optional
from ..models import Patient
from .base_service import BaseService
from datetime import date

class PatientService(BaseService[Patient]):
    def create_patient(self, 
                      name: str,
                      date_of_birth: date,
                      gender: str,
                      blood_group: str,
                      contact_number: str,
                      email: str,
                      address: str,
                      insurance_details: dict = None) -> Optional[Patient]:
        patient_id = self._generate_id("PAT", "patients")
        
        query = """
        INSERT INTO patients (
            patient_id, name, date_of_birth, gender, blood_group,
            contact_number, email, address, insurance_details
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            patient_id, name, date_of_birth, gender, blood_group,
            contact_number, email, address, str(insurance_details)
        )
        
        if self._execute_query(query, params) is not None:
            return self.get_patient_by_id(patient_id)
        return None

    def get_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        query = "SELECT * FROM patients WHERE patient_id = %s"
        result = self._execute_query(query, (patient_id,))
        
        if result and len(result) > 0:
            return Patient.from_db_dict(result[0])
        return None

    def get_all_patients(self) -> List[Patient]:
        query = "SELECT * FROM patients"
        result = self._execute_query(query)
        
        return [Patient.from_db_dict(row) for row in (result or [])]

    def update_patient(self, patient: Patient) -> bool:
        query = """
        UPDATE patients 
        SET name = %s, date_of_birth = %s, gender = %s, blood_group = %s,
            contact_number = %s, email = %s, address = %s, insurance_details = %s
        WHERE patient_id = %s
        """
        params = (
            patient.name, patient.date_of_birth, patient.gender, patient.blood_group,
            patient.contact_number, patient.email, patient.address,
            str(patient.insurance_details), patient.patient_id
        )
        
        return self._execute_query(query, params) is not None

    def delete_patient(self, patient_id: str) -> bool:
        query = "DELETE FROM patients WHERE patient_id = %s"
        return self._execute_query(query, (patient_id,)) is not None

    def search_patients(self, search_term: str) -> List[Patient]:
        query = """
        SELECT * FROM patients 
        WHERE name LIKE %s 
        OR contact_number LIKE %s 
        OR email LIKE %s
        """
        search_pattern = f"%{search_term}%"
        params = (search_pattern, search_pattern, search_pattern)
        
        result = self._execute_query(query, params)
        return [Patient.from_db_dict(row) for row in (result or [])]

    def get_patient_medical_history(self, patient_id: str) -> List[dict]:
        query = """
        SELECT mr.*, d.name as doctor_name 
        FROM medical_records mr
        JOIN doctors d ON mr.doctor_id = d.doctor_id
        WHERE mr.patient_id = %s
        ORDER BY mr.visit_date DESC
        """
        result = self._execute_query(query, (patient_id,))
        return result or []
