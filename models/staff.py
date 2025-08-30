from datetime import date
from typing import Dict, Optional

class Staff:
    def __init__(
        self,
        staff_id: str,
        name: str,
        role: str,
        department_id: int,
        contact_number: str,
        email: str,
        date_joined: date
    ):
        self.staff_id = staff_id
        self.name = name
        self.role = role
        self.department_id = department_id
        self.contact_number = contact_number
        self.email = email
        self.date_joined = date_joined

    @staticmethod
    def from_db_dict(data: Dict) -> 'Staff':
        return Staff(
            staff_id=data['staff_id'],
            name=data['name'],
            role=data['role'],
            department_id=data['department_id'],
            contact_number=data['contact_number'],
            email=data['email'],
            date_joined=data['date_joined']
        )

    def to_dict(self) -> Dict:
        return {
            'staff_id': self.staff_id,
            'name': self.name,
            'role': self.role,
            'department_id': self.department_id,
            'contact_number': self.contact_number,
            'email': self.email,
            'date_joined': self.date_joined
        }
