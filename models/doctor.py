from typing import Dict, List
from datetime import date
from .staff import Staff

class Doctor(Staff):
    def __init__(
        self,
        staff_id: str,
        name: str,
        department_id: int,
        contact_number: str,
        email: str,
        date_joined: date,
        doctor_id: str,
        specialization: str,
        qualifications: List[str],
        consultation_fee: float,
        consultation_room: str = None
    ):
        super().__init__(
            staff_id=staff_id,
            name=name,
            role="Doctor",
            department_id=department_id,
            contact_number=contact_number,
            email=email,
            date_joined=date_joined
        )
        self.doctor_id = doctor_id
        self.specialization = specialization
        self.qualifications = qualifications
        self.consultation_fee = consultation_fee
        self.consultation_room = consultation_room
        self.availability_schedule = {}

    @staticmethod
    def from_db_dict(data: Dict) -> 'Doctor':
        # Convert string qualifications to list
        qualifications_str = data.get('qualification', '') or data.get('qualifications', '')
        qualifications = [q.strip() for q in qualifications_str.split(',')] if qualifications_str else []
        
        # Handle potential None values and type conversions
        try:
            return Doctor(
                staff_id=data['staff_id'],
                name=data['name'],
                department_id=data['department_id'],
                contact_number=data.get('contact_number', ''),
                email=data.get('email', ''),
                date_joined=data['date_joined'],
                doctor_id=data['doctor_id'],
                specialization=data.get('specialization', ''),
                qualifications=qualifications,
                consultation_fee=float(data.get('consultation_fee', 0))
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")

    def to_dict(self) -> Dict:
        base_dict = super().to_dict()
        doctor_dict = {
            'doctor_id': self.doctor_id,
            'specialization': self.specialization,
            'qualifications': ','.join(self.qualifications),
            'consultation_fee': self.consultation_fee,
            'consultation_room': self.consultation_room
        }
        return {**base_dict, **doctor_dict}

    def update_schedule(self, schedule: Dict):
        self.availability_schedule = schedule

    def is_available(self, date_time) -> bool:
        # Convert date_time to appropriate format and check availability
        date_str = date_time.strftime('%Y-%m-%d')
        time_str = date_time.strftime('%H:%M')
        
        if date_str in self.availability_schedule:
            available_times = self.availability_schedule[date_str]
            return time_str in available_times
        return False
