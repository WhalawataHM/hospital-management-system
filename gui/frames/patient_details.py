import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from ..base_frame import BaseFrame
from ...services import PatientService, AppointmentService, MedicalRecordService

class PatientDetailsFrame(BaseFrame):
    def __init__(self, parent, controller):
        self.patient_service = PatientService()
        self.appointment_service = AppointmentService()
        self.medical_record_service = MedicalRecordService()
        super().__init__(parent, controller)

    def init_ui(self):
        # Create main content frame
        content = ttk.Frame(self)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Header frame
        header_frame = ttk.Frame(content)
        header_frame.pack(fill="x", pady=(0, 20))

        # Back button
        back_btn = ttk.Button(
            header_frame,
            text="Back to List",
            command=lambda: self.controller.show_frame("PatientList")
        )
        back_btn.pack(side="left")

        self.title_label = ttk.Label(
            header_frame,
            text="New Patient",
            style="Header.TLabel"
        )
        self.title_label.pack(side="left", padx=20)

        # Save button
        self.save_btn = ttk.Button(
            header_frame,
            text="Save",
            command=self.save_patient
        )
        self.save_btn.pack(side="right")

        # Create form
        form_frame = ttk.LabelFrame(content, text="Patient Information")
        form_frame.pack(fill="x", pady=10)

        # Configure grid
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # Patient details
        current_row = 0

        # Name
        ttk.Label(form_frame, text="Name:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var)
        self.name_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")

        # Gender
        ttk.Label(form_frame, text="Gender:").grid(row=current_row, column=2, padx=5, pady=5, sticky="e")
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(form_frame, textvariable=self.gender_var, values=["Male", "Female", "Other"])
        gender_combo.grid(row=current_row, column=3, padx=5, pady=5, sticky="ew")

        current_row += 1

        # Date of Birth
        ttk.Label(form_frame, text="Date of Birth:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.dob_entry = DateEntry(form_frame, width=12, background='darkblue',
                                 foreground='white', borderwidth=2)
        self.dob_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")

        # Blood Group
        ttk.Label(form_frame, text="Blood Group:").grid(row=current_row, column=2, padx=5, pady=5, sticky="e")
        self.blood_group_var = tk.StringVar()
        blood_group_combo = ttk.Combobox(form_frame, textvariable=self.blood_group_var,
                                       values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        blood_group_combo.grid(row=current_row, column=3, padx=5, pady=5, sticky="ew")

        current_row += 1

        # Contact
        ttk.Label(form_frame, text="Contact:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.contact_var = tk.StringVar()
        self.contact_entry = ttk.Entry(form_frame, textvariable=self.contact_var)
        self.contact_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")

        # Email
        ttk.Label(form_frame, text="Email:").grid(row=current_row, column=2, padx=5, pady=5, sticky="e")
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(form_frame, textvariable=self.email_var)
        self.email_entry.grid(row=current_row, column=3, padx=5, pady=5, sticky="ew")

        current_row += 1

        # Address
        ttk.Label(form_frame, text="Address:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.address_text = tk.Text(form_frame, height=3, width=40)
        self.address_text.grid(row=current_row, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Tabs for Appointments and Medical Records
        tab_control = ttk.Notebook(content)
        tab_control.pack(fill="both", expand=True, pady=10)

        # Appointments tab
        appointments_frame = ttk.Frame(tab_control)
        tab_control.add(appointments_frame, text="Appointments")

        # Appointments table
        self.appointments_table = self.create_table(
            appointments_frame,
            {
                "date": 150,
                "doctor": 200,
                "department": 150,
                "status": 100
            }
        )

        # Medical Records tab
        records_frame = ttk.Frame(tab_control)
        tab_control.add(records_frame, text="Medical Records")

        # Medical Records table
        self.records_table = self.create_table(
            records_frame,
            {
                "date": 150,
                "doctor": 200,
                "diagnosis": 300,
                "prescriptions": 200
            }
        )

    def on_show(self):
        if hasattr(self.controller, "current_patient_id"):
            self.load_patient(self.controller.current_patient_id)
        else:
            self.clear_form()

    def load_patient(self, patient_id):
        patient = self.patient_service.get_patient_by_id(patient_id)
        if patient:
            self.title_label.config(text=f"Patient: {patient.name}")
            self.name_var.set(patient.name)
            self.gender_var.set(patient.gender)
            self.dob_entry.set_date(patient.date_of_birth)
            self.blood_group_var.set(patient.blood_group)
            self.contact_var.set(patient.contact_number)
            self.email_var.set(patient.email)
            self.address_text.delete("1.0", tk.END)
            self.address_text.insert("1.0", patient.address)

            # Load appointments
            self.load_appointments(patient_id)

            # Load medical records
            self.load_medical_records(patient_id)

    def load_appointments(self, patient_id):
        self.appointments_table.delete(*self.appointments_table.get_children())
        appointments = self.appointment_service.get_appointments_by_patient(patient_id)
        
        for apt in appointments:
            self.appointments_table.insert(
                "",
                "end",
                values=(
                    apt.date_time.strftime("%Y-%m-%d %H:%M"),
                    apt.doctor_name,
                    apt.department,
                    apt.status
                )
            )

    def load_medical_records(self, patient_id):
        self.records_table.delete(*self.records_table.get_children())
        records = self.medical_record_service.get_patient_records(patient_id)
        
        for record in records:
            self.records_table.insert(
                "",
                "end",
                values=(
                    record.visit_date.strftime("%Y-%m-%d"),
                    record.doctor_name,
                    record.diagnosis,
                    ", ".join(record.prescriptions)
                )
            )

    def clear_form(self):
        self.title_label.config(text="New Patient")
        self.name_var.set("")
        self.gender_var.set("")
        self.dob_entry.set_date(datetime.now())
        self.blood_group_var.set("")
        self.contact_var.set("")
        self.email_var.set("")
        self.address_text.delete("1.0", tk.END)
        
        # Clear tables
        self.appointments_table.delete(*self.appointments_table.get_children())
        self.records_table.delete(*self.records_table.get_children())

    def save_patient(self):
        # Validate required fields
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Name is required")
            return

        patient_data = {
            "name": self.name_var.get().strip(),
            "gender": self.gender_var.get(),
            "date_of_birth": self.dob_entry.get_date(),
            "blood_group": self.blood_group_var.get(),
            "contact_number": self.contact_var.get().strip(),
            "email": self.email_var.get().strip(),
            "address": self.address_text.get("1.0", tk.END).strip()
        }

        try:
            if hasattr(self.controller, "current_patient_id"):
                # Update existing patient
                patient_data["patient_id"] = self.controller.current_patient_id
                success = self.patient_service.update_patient(patient_data)
                if success:
                    messagebox.showinfo("Success", "Patient updated successfully")
            else:
                # Create new patient
                patient = self.patient_service.create_patient(**patient_data)
                if patient:
                    messagebox.showinfo("Success", "Patient created successfully")
                    self.controller.current_patient_id = patient.patient_id

            # Return to patient list
            self.controller.show_frame("PatientList")

        except Exception as e:
            messagebox.showerror("Error", str(e))
