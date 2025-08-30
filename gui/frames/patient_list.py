import tkinter as tk
from tkinter import ttk, messagebox
from ..base_frame import BaseFrame
from ...services import PatientService

class PatientListFrame(BaseFrame):
    def __init__(self, parent, controller):
        self.patient_service = PatientService()
        super().__init__(parent, controller)

    def init_ui(self):
        # Create main content frame
        content = ttk.Frame(self)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Header frame
        header_frame = ttk.Frame(content)
        header_frame.pack(fill="x", pady=(0, 20))

        # Title
        title = ttk.Label(
            header_frame,
            text="Patients",
            style="Header.TLabel"
        )
        title.pack(side="left")

        # Add Patient button
        add_btn = ttk.Button(
            header_frame,
            text="Add Patient",
            command=self.add_patient
        )
        add_btn.pack(side="right")

        # Search frame
        search_frame = ttk.Frame(content)
        search_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True)

        # Create table
        self.table = self.create_table(
            content,
            {
                "id": 100,
                "name": 200,
                "age": 80,
                "gender": 100,
                "contact": 150,
                "email": 200,
                "blood_group": 100
            },
            height=15
        )

        # Bind double click event
        self.table.bind("<Double-1>", self.on_patient_select)

    def on_show(self):
        self.load_patients()

    def load_patients(self):
        # Clear existing items
        self.table.delete(*self.table.get_children())

        # Get all patients
        patients = self.patient_service.get_all_patients()
        
        for patient in patients:
            age = self.calculate_age(patient.date_of_birth)
            self.table.insert(
                "",
                "end",
                values=(
                    patient.patient_id,
                    patient.name,
                    age,
                    patient.gender,
                    patient.contact_number,
                    patient.email,
                    patient.blood_group
                )
            )

    def on_search_change(self, *args):
        search_term = self.search_var.get().strip()
        if search_term:
            patients = self.patient_service.search_patients(search_term)
        else:
            patients = self.patient_service.get_all_patients()

        # Clear and reload table
        self.table.delete(*self.table.get_children())
        for patient in patients:
            age = self.calculate_age(patient.date_of_birth)
            self.table.insert(
                "",
                "end",
                values=(
                    patient.patient_id,
                    patient.name,
                    age,
                    patient.gender,
                    patient.contact_number,
                    patient.email,
                    patient.blood_group
                )
            )

    def add_patient(self):
        self.controller.show_frame("PatientDetails")

    def on_patient_select(self, event):
        selected_item = self.table.selection()
        if not selected_item:
            return

        patient_id = self.table.item(selected_item[0])["values"][0]
        # Store the selected patient ID and show details frame
        self.controller.current_patient_id = patient_id
        self.controller.show_frame("PatientDetails")

    @staticmethod
    def calculate_age(birth_date):
        from datetime import date
        today = date.today()
        age = (today.year - birth_date.year -
               ((today.month, today.day) < (birth_date.month, birth_date.day)))
        return age
