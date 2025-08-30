from typing import Dict, List
from datetime import date

class MedicalRecord:
    def __init__(
        self,
        record_id: str,
        patient_id: str,
        doctor_id: str,
        visit_date: date,
        diagnosis: str,
        prescriptions: List[str],
        test_results: List[Dict] = None,
        notes: str = None
    ):
        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.visit_date = visit_date
        self.diagnosis = diagnosis
        self.prescriptions = prescriptions
        self.test_results = test_results or []
        self.notes = notes

    @staticmethod
    def from_db_dict(data: Dict) -> 'MedicalRecord':
        prescriptions = eval(data['prescription']) if data['prescription'] else []
        return MedicalRecord(
            record_id=data['record_id'],
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            visit_date=data['visit_date'],
            diagnosis=data['diagnosis'],
            prescriptions=prescriptions,
            notes=data.get('notes')
        )

    def to_dict(self) -> Dict:
        return {
            'record_id': self.record_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'visit_date': self.visit_date,
            'diagnosis': self.diagnosis,
            'prescription': str(self.prescriptions),
            'notes': self.notes
        }

    def add_prescription(self, prescription: str):
        self.prescriptions.append(prescription)

    def add_test_result(self, test_result: Dict):
        self.test_results.append(test_result)

    def update_diagnosis(self, diagnosis: str):
        self.diagnosis = diagnosis

    def add_notes(self, notes: str):
        if self.notes:
            self.notes += f"\n{notes}"
        else:
            self.notes = notes

    def generate_report(self) -> Dict:
        return {
            'record_id': self.record_id,
            'visit_date': self.visit_date.strftime('%Y-%m-%d'),
            'diagnosis': self.diagnosis,
            'prescriptions': self.prescriptions,
            'test_results': self.test_results,
            'notes': self.notes
        }
