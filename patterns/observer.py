from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: dict):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(event_type, data)

class EmailNotifier(Observer):
    def update(self, event_type: str, data: dict):
        # In a real system, this would send an actual email
        print(f"EMAIL NOTIFICATION: {event_type}")
        print(f"To: {data.get('email', 'no-email')}")
        print(f"Subject: Hospital Management System - {event_type}")
        print(f"Message: {self._generate_message(event_type, data)}\n")

    def _generate_message(self, event_type: str, data: dict) -> str:
        if event_type == "APPOINTMENT_SCHEDULED":
            return (f"Your appointment has been scheduled for {data.get('date_time')} "
                   f"with Dr. {data.get('doctor_name')}")
        elif event_type == "APPOINTMENT_CANCELLED":
            return f"Your appointment for {data.get('date_time')} has been cancelled"
        return f"Event: {event_type} - Details: {data}"

class SMSNotifier(Observer):
    def update(self, event_type: str, data: dict):
        # In a real system, this would send an actual SMS
        print(f"SMS NOTIFICATION: {event_type}")
        print(f"To: {data.get('phone', 'no-phone')}")
        print(f"Message: {self._generate_message(event_type, data)}\n")

    def _generate_message(self, event_type: str, data: dict) -> str:
        if event_type == "APPOINTMENT_SCHEDULED":
            return (f"Appt scheduled: {data.get('date_time')} "
                   f"with Dr. {data.get('doctor_name')}")
        elif event_type == "APPOINTMENT_CANCELLED":
            return f"Appt cancelled: {data.get('date_time')}"
        return f"{event_type}: {data}"

class SystemLogger(Observer):
    def update(self, event_type: str, data: dict):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"SYSTEM LOG [{timestamp}] {event_type}")
        print(f"Details: {data}\n")

class AppointmentSystem(Subject):
    def schedule_appointment(self, patient_data: dict, doctor_data: dict, 
                           date_time: datetime):
        # Logic to schedule appointment in database would go here
        
        notification_data = {
            "appointment_id": "AP" + datetime.now().strftime("%Y%m%d%H%M%S"),
            "patient_name": patient_data.get("name"),
            "patient_id": patient_data.get("id"),
            "email": patient_data.get("email"),
            "phone": patient_data.get("phone"),
            "doctor_name": doctor_data.get("name"),
            "doctor_id": doctor_data.get("id"),
            "date_time": date_time.strftime("%Y-%m-%d %H:%M"),
            "status": "SCHEDULED"
        }
        
        self.notify("APPOINTMENT_SCHEDULED", notification_data)
        return notification_data["appointment_id"]

    def cancel_appointment(self, appointment_id: str, reason: str):
        # Logic to cancel appointment in database would go here
        
        notification_data = {
            "appointment_id": appointment_id,
            "reason": reason,
            "status": "CANCELLED"
        }
        
        self.notify("APPOINTMENT_CANCELLED", notification_data)
