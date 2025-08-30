from typing import Dict, List, Optional
from datetime import date

from hospital_management_system.models.medical_record import MedicalRecord

class Patient:
    def __init__(
        self,
        patient_id: str,
        name: str,
        date_of_birth: date,
        gender: str,
        blood_group: str,
        contact_number: str,
        email: str,
        address: str,
        insurance_details: Optional[Dict] = None
    ):
        self.patient_id = patient_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.blood_group = blood_group
        self.contact_number = contact_number
        self.email = email
        self.address = address
        self.insurance_details = insurance_details or {}
        self.medical_history: List = []

    @staticmethod
    def from_db_dict(data: Dict) -> 'Patient':
        insurance_details = eval(data['insurance_details']) if data['insurance_details'] else {}
        return Patient(
            patient_id=data['patient_id'],
            name=data['name'],
            date_of_birth=data['date_of_birth'],
            gender=data['gender'],
            blood_group=data['blood_group'],
            contact_number=data['contact_number'],
            email=data['email'],
            address=data['address'],
            insurance_details=insurance_details
        )

    def to_dict(self) -> Dict:
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'blood_group': self.blood_group,
            'contact_number': self.contact_number,
            'email': self.email,
            'address': self.address,
            'insurance_details': str(self.insurance_details)
        }

    def add_medical_record(self, record: 'MedicalRecord'):
        self.medical_history.append(record)

    def get_medical_history(self) -> List['MedicalRecord']:
        return sorted(self.medical_history, key=lambda x: x.visit_date, reverse=True)

    def update_insurance(self, insurance_details: Dict):
        self.insurance_details = insurance_details
