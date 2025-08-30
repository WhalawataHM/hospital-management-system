import tkinter as tk
from tkinter import ttk, messagebox
from ..base_frame import BaseFrame
from ...services import DoctorService

class DoctorListFrame(BaseFrame):
    def __init__(self, parent, controller):
        self.doctor_service = DoctorService()
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
            text="Doctors",
            style="Header.TLabel"
        )
        title.pack(side="left")

        # Add Doctor button
        add_btn = ttk.Button(
            header_frame,
            text="Add Doctor",
            command=self.add_doctor
        )
        add_btn.pack(side="right")

        # Search frame
        search_frame = ttk.Frame(content)
        search_frame.pack(fill="x", pady=(0, 20))

        # Search by name
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True)

        # Filter by specialization
        ttk.Label(search_frame, text="Specialization:").pack(side="left", padx=5)
        self.specialization_var = tk.StringVar()
        self.specialization_var.trace("w", self.on_filter_change)
        self.specialization_combo = ttk.Combobox(
            search_frame,
            textvariable=self.specialization_var,
            width=20
        )
        self.specialization_combo.pack(side="left", padx=5)

        # Create table
        self.table = self.create_table(
            content,
            {
                "id": 100,
                "name": 200,
                "specialization": 200,
                "qualification": 200,
                "contact": 150,
                "email": 200,
                "fee": 100
            },
            height=15
        )

        # Bind double click event
        self.table.bind("<Double-1>", self.on_doctor_select)

    def on_show(self):
        self.load_doctors()
        self.load_specializations()

    def load_doctors(self):
        # Clear existing items
        self.table.delete(*self.table.get_children())

        # Get all doctors
        doctors = self.doctor_service.get_all_doctors()
        
        for doctor in doctors:
            self.table.insert(
                "",
                "end",
                values=(
                    doctor.doctor_id,
                    doctor.name,
                    doctor.specialization,
                    ", ".join(doctor.qualifications),
                    doctor.contact_number,
                    doctor.email,
                    f"${doctor.consultation_fee:.2f}"
                )
            )

    def load_specializations(self):
        # Get unique specializations
        doctors = self.doctor_service.get_all_doctors()
        specializations = sorted(set(doc.specialization for doc in doctors))
        self.specialization_combo['values'] = ["All"] + specializations
        self.specialization_var.set("All")

    def on_search_change(self, *args):
        self.filter_doctors()

    def on_filter_change(self, *args):
        self.filter_doctors()

    def filter_doctors(self):
        search_term = self.search_var.get().strip()
        specialization = self.specialization_var.get()
        
        # Get all doctors first
        if search_term:
            doctors = self.doctor_service.search_doctors(search_term)
        else:
            doctors = self.doctor_service.get_all_doctors()

        # Apply specialization filter
        if specialization and specialization != "All":
            doctors = [doc for doc in doctors if doc.specialization == specialization]

        # Clear and reload table
        self.table.delete(*self.table.get_children())
        for doctor in doctors:
            self.table.insert(
                "",
                "end",
                values=(
                    doctor.doctor_id,
                    doctor.name,
                    doctor.specialization,
                    ", ".join(doctor.qualifications),
                    doctor.contact_number,
                    doctor.email,
                    f"${doctor.consultation_fee:.2f}"
                )
            )

    def add_doctor(self):
        # Clear current doctor selection
        if hasattr(self.controller, "current_doctor_id"):
            delattr(self.controller, "current_doctor_id")
        self.controller.show_frame("DoctorDetails")

    def on_doctor_select(self, event):
        selected_item = self.table.selection()
        if not selected_item:
            return

        doctor_id = self.table.item(selected_item[0])["values"][0]
        # Store the selected doctor ID and show details frame
        self.controller.current_doctor_id = doctor_id
        self.controller.show_frame("DoctorDetails")
