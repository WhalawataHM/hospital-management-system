import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ..base_frame import BaseFrame
from ...services import PatientService, DoctorService, AppointmentService

class DashboardFrame(BaseFrame):
    def __init__(self, parent, controller):
        self.patient_service = PatientService()
        self.doctor_service = DoctorService()
        self.appointment_service = AppointmentService()
        super().__init__(parent, controller)

    def init_ui(self):
        # Create main content frame
        content = ttk.Frame(self)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ttk.Label(
            content,
            text="Dashboard",
            style="Header.TLabel"
        )
        title.pack(pady=(0, 20))

        # Create cards frame
        cards_frame = ttk.Frame(content)
        cards_frame.pack(fill="x", pady=10)
        
        # Statistics cards
        self.create_stat_card(cards_frame, "Total Patients", "patient_count", 0)
        self.create_stat_card(cards_frame, "Total Doctors", "doctor_count", 1)
        self.create_stat_card(cards_frame, "Today's Appointments", "appointment_count", 2)

        # Create bottom frame for tables
        bottom_frame = ttk.Frame(content)
        bottom_frame.pack(fill="both", expand=True, pady=10)

        # Recent appointments
        appointments_frame = ttk.LabelFrame(bottom_frame, text="Recent Appointments")
        appointments_frame.pack(fill="both", expand=True, side="left", padx=5)
        
        self.appointments_table = self.create_table(
            appointments_frame,
            {
                "time": 100,
                "patient": 150,
                "doctor": 150,
                "status": 100
            }
        )

        # Available doctors
        doctors_frame = ttk.LabelFrame(bottom_frame, text="Available Doctors")
        doctors_frame.pack(fill="both", expand=True, side="right", padx=5)
        
        self.doctors_table = self.create_table(
            doctors_frame,
            {
                "name": 150,
                "specialization": 150,
                "status": 100
            }
        )

    def create_stat_card(self, parent, title, tag, column):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.grid(row=0, column=column, padx=10, sticky="nsew")
        
        ttk.Label(
            card,
            text=title,
            style="Navigation.TButton"
        ).pack(pady=(10, 5))
        
        value = ttk.Label(
            card,
            text="0",
            style="Header.TLabel"
        )
        value.pack(pady=(5, 10))
        
        # Store the label reference for updating
        setattr(self, f"{tag}_label", value)

    def on_show(self):
        # Update statistics
        self.update_statistics()
        # Update tables
        self.update_tables()

    def update_statistics(self):
        # Update patient count
        patients = self.patient_service.get_all_patients()
        self.patient_count_label["text"] = str(len(patients))

        # Update doctor count
        doctors = self.doctor_service.get_all_doctors()
        self.doctor_count_label["text"] = str(len(doctors))

        # Update today's appointments
        today = datetime.now().date()
        appointments = self.appointment_service.get_appointments_by_date(today)
        self.appointment_count_label["text"] = str(len(appointments))

    def update_tables(self):
        # Clear existing items
        self.appointments_table.delete(*self.appointments_table.get_children())
        self.doctors_table.delete(*self.doctors_table.get_children())

        # Get recent appointments
        appointments = self.appointment_service.get_recent_appointments()
        for apt in appointments:
            self.appointments_table.insert(
                "",
                "end",
                values=(
                    apt.date_time.strftime("%H:%M"),
                    apt.patient_name,
                    apt.doctor_name,
                    apt.status
                )
            )

        # Get available doctors
        doctors = self.doctor_service.get_available_doctors()
        for doc in doctors:
            self.doctors_table.insert(
                "",
                "end",
                values=(
                    doc.name,
                    doc.specialization,
                    "Available"
                )
            )
