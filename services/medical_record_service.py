from typing import List, Optional, Dict
from datetime import date
from ..models import MedicalRecord
from .base_service import BaseService

class MedicalRecordService(BaseService[MedicalRecord]):
    def create_record(self,
                     patient_id: str,
                     doctor_id: str,
                     diagnosis: str,
                     prescriptions: List[str],
                     notes: str = None) -> Optional[MedicalRecord]:
        record_id = self._generate_id("MR", "medical_records")
        
        query = """
        INSERT INTO medical_records (
            record_id, patient_id, doctor_id, visit_date,
            diagnosis, prescription, notes
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            record_id, patient_id, doctor_id, date.today(),
            diagnosis, str(prescriptions), notes
        )
        
        if self._execute_query(query, params) is not None:
            return self.get_record_by_id(record_id)
        return None

    def get_record_by_id(self, record_id: str) -> Optional[MedicalRecord]:
        query = """
        SELECT * FROM medical_records WHERE record_id = %s
        """
        result = self._execute_query(query, (record_id,))
        
        if result and len(result) > 0:
            return MedicalRecord.from_db_dict(result[0])
        return None

    def get_patient_records(self, patient_id: str) -> List[MedicalRecord]:
        query = """
        SELECT mr.*, d.name as doctor_name
        FROM medical_records mr
        JOIN doctors doc ON mr.doctor_id = doc.doctor_id
        JOIN staff d ON doc.staff_id = d.staff_id
        WHERE mr.patient_id = %s
        ORDER BY mr.visit_date DESC
        """
        result = self._execute_query(query, (patient_id,))
        return [MedicalRecord.from_db_dict(row) for row in (result or [])]

    def search_records(self, patient_search: Optional[str] = None,
                      doctor_search: Optional[str] = None,
                      start_date: Optional[date] = None,
                      end_date: Optional[date] = None) -> List[MedicalRecord]:
        query = """
        SELECT mr.*, p.name as patient_name, d.name as doctor_name
        FROM medical_records mr
        JOIN doctors doc ON mr.doctor_id = doc.doctor_id
        JOIN staff d ON doc.staff_id = d.staff_id
        JOIN patients p ON mr.patient_id = p.patient_id
        WHERE 1=1
        """
        params = []

        if patient_search:
            query += " AND p.name LIKE %s"
            params.append(f"%{patient_search}%")

        if doctor_search:
            query += " AND d.name LIKE %s"
            params.append(f"%{doctor_search}%")

        if start_date and end_date:
            query += " AND mr.visit_date BETWEEN %s AND %s"
            params.extend([start_date, end_date])

        query += " ORDER BY mr.visit_date DESC"
        result = self._execute_query(query, tuple(params) if params else None)
        return [MedicalRecord.from_db_dict(row) for row in (result or [])]

    def get_doctor_records(self, doctor_id: str) -> List[MedicalRecord]:
        query = """
        SELECT mr.*, p.name as patient_name
        FROM medical_records mr
        JOIN patients p ON mr.patient_id = p.patient_id
        WHERE mr.doctor_id = %s
        ORDER BY mr.visit_date DESC
        """
        result = self._execute_query(query, (doctor_id,))
        return [MedicalRecord.from_db_dict(row) for row in (result or [])]

    def update_record(self, record: MedicalRecord) -> bool:
        query = """
        UPDATE medical_records 
        SET diagnosis = %s, prescription = %s, notes = %s
        WHERE record_id = %s
        """
        params = (
            record.diagnosis,
            str(record.prescriptions),
            record.notes,
            record.record_id
        )
        return self._execute_query(query, params) is not None

    def add_prescription(self, record_id: str, prescription: str) -> bool:
        record = self.get_record_by_id(record_id)
        if not record:
            return False
            
        record.add_prescription(prescription)
        return self.update_record(record)

    def add_notes(self, record_id: str, notes: str) -> bool:
        record = self.get_record_by_id(record_id)
        if not record:
            return False
            
        record.add_notes(notes)
        return self.update_record(record)

    def generate_patient_report(self, patient_id: str) -> Dict:
        records = self.get_patient_records(patient_id)
        return {
            'patient_id': patient_id,
            'total_visits': len(records),
            'records': [record.generate_report() for record in records]
        }
