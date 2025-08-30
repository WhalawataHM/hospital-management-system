import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
from ..base_frame import BaseFrame
from ...services import DoctorService, AppointmentService

class DoctorDetailsFrame(BaseFrame):
    def __init__(self, parent, controller):
        self.doctor_service = DoctorService()
        self.appointment_service = AppointmentService()
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
            command=lambda: self.controller.show_frame("DoctorList")
        )
        back_btn.pack(side="left")

        self.title_label = ttk.Label(
            header_frame,
            text="New Doctor",
            style="Header.TLabel"
        )
        self.title_label.pack(side="left", padx=20)

        # Save button
        self.save_btn = ttk.Button(
            header_frame,
            text="Save",
            command=self.save_doctor
        )
        self.save_btn.pack(side="right")

        # Create form
        form_frame = ttk.LabelFrame(content, text="Doctor Information")
        form_frame.pack(fill="x", pady=10)

        # Configure grid
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        current_row = 0

        # Basic Information
        # Name
        ttk.Label(form_frame, text="Name:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var)
        self.name_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")

        # Department
        ttk.Label(form_frame, text="Department:").grid(row=current_row, column=2, padx=5, pady=5, sticky="e")
        self.department_var = tk.StringVar()
        self.department_combo = ttk.Combobox(form_frame, textvariable=self.department_var)
        self.department_combo.grid(row=current_row, column=3, padx=5, pady=5, sticky="ew")

        current_row += 1

        # Specialization
        ttk.Label(form_frame, text="Specialization:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.specialization_var = tk.StringVar()
        self.specialization_entry = ttk.Entry(form_frame, textvariable=self.specialization_var)
        self.specialization_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")

        # Consultation Fee
        ttk.Label(form_frame, text="Consultation Fee:").grid(row=current_row, column=2, padx=5, pady=5, sticky="e")
        self.fee_var = tk.StringVar()
        fee_entry = ttk.Entry(form_frame, textvariable=self.fee_var)
        fee_entry.grid(row=current_row, column=3, padx=5, pady=5, sticky="ew")

        current_row += 1

        # Contact Information
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

        # Qualifications
        ttk.Label(form_frame, text="Qualifications:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.qualifications_text = tk.Text(form_frame, height=3, width=40)
        self.qualifications_text.grid(row=current_row, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Tabs for Schedule and Appointments
        tab_control = ttk.Notebook(content)
        tab_control.pack(fill="both", expand=True, pady=10)

        # Schedule tab
        schedule_frame = ttk.Frame(tab_control)
        tab_control.add(schedule_frame, text="Schedule")

        # Create schedule management interface
        self._create_schedule_interface(schedule_frame)

        # Appointments tab
        appointments_frame = ttk.Frame(tab_control)
        tab_control.add(appointments_frame, text="Appointments")

        # Appointments table
        self.appointments_table = self.create_table(
            appointments_frame,
            {
                "date": 150,
                "time": 100,
                "patient": 200,
                "status": 100
            }
        )

    def _create_schedule_interface(self, parent):
        # Date selection
        date_frame = ttk.Frame(parent)
        date_frame.pack(fill="x", pady=10)
        
        ttk.Label(date_frame, text="Select Date:").pack(side="left", padx=5)
        self.schedule_date = DateEntry(date_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2)
        self.schedule_date.pack(side="left", padx=5)
        
        ttk.Button(
            date_frame,
            text="View Schedule",
            command=self.load_schedule
        ).pack(side="left", padx=5)

        # Time slots frame
        time_slots_frame = ttk.LabelFrame(parent, text="Available Time Slots")
        time_slots_frame.pack(fill="both", expand=True, pady=10)

        # Create time slots grid
        self.time_slots = {}
        current_row = 0
        times = [
            "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
            "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
        ]

        for i, time in enumerate(times):
            row = i // 4
            col = i % 4
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(time_slots_frame, text=time, variable=var)
            cb.grid(row=row, column=col, padx=10, pady=5)
            self.time_slots[time] = var

    def load_schedule(self):
        if not hasattr(self.controller, "current_doctor_id"):
            return

        selected_date = self.schedule_date.get_date()
        appointments = self.doctor_service.get_doctor_schedule(
            self.controller.current_doctor_id,
            selected_date
        )

        # Reset all checkboxes
        for var in self.time_slots.values():
            var.set(False)

        # Mark booked slots
        for apt in appointments:
            time = apt['appointment_date'].strftime("%H:%M")
            if time in self.time_slots:
                self.time_slots[time].set(True)

    def on_show(self):
        # Load departments for dropdown
        self.load_departments()
        
        if hasattr(self.controller, "current_doctor_id"):
            self.load_doctor(self.controller.current_doctor_id)
        else:
            self.clear_form()

    def load_departments(self):
        try:
            # Get departments from the service
            departments = self.doctor_service.get_departments()
            
            if departments:
                self.departments = {dept['name']: dept['department_id'] for dept in departments}
            else:
                # If no departments found, use some defaults
                self.departments = {
                    "General Medicine": 1,
                    "Cardiology": 2,
                    "Pediatrics": 3,
                    "Orthopedics": 4,
                    "Neurology": 5
                }
            
            self.department_combo['values'] = list(self.departments.keys())
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load departments: {str(e)}")
            self.departments = {}

    def load_doctor(self, doctor_id):
        doctor = self.doctor_service.get_doctor_by_id(doctor_id)
        if doctor:
            self.title_label.config(text=f"Doctor: {doctor.name}")
            self.name_var.set(doctor.name)
            self.department_var.set(doctor.department_id)  # You'll need to convert ID to name
            self.specialization_var.set(doctor.specialization)
            self.fee_var.set(str(doctor.consultation_fee))
            self.contact_var.set(doctor.contact_number)
            self.email_var.set(doctor.email)
            self.qualifications_text.delete("1.0", tk.END)
            self.qualifications_text.insert("1.0", "\n".join(doctor.qualifications))

            # Load appointments
            self.load_appointments(doctor_id)

    def load_appointments(self, doctor_id):
        self.appointments_table.delete(*self.appointments_table.get_children())
        appointments = self.appointment_service.get_appointments_by_doctor(doctor_id)
        
        for apt in appointments:
            self.appointments_table.insert(
                "",
                "end",
                values=(
                    apt.date_time.strftime("%Y-%m-%d"),
                    apt.date_time.strftime("%H:%M"),
                    apt.patient_name,
                    apt.status
                )
            )

    def clear_form(self):
        self.title_label.config(text="New Doctor")
        self.name_var.set("")
        self.department_var.set("")
        self.specialization_var.set("")
        self.fee_var.set("")
        self.contact_var.set("")
        self.email_var.set("")
        self.qualifications_text.delete("1.0", tk.END)
        self.appointments_table.delete(*self.appointments_table.get_children())

    def save_doctor(self):
        # Validate required fields
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Name is required")
            return

        if not self.specialization_var.get().strip():
            messagebox.showerror("Error", "Specialization is required")
            return

        try:
            fee = float(self.fee_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid consultation fee")
            return

        # Get qualifications as list
        qualifications = [
            q.strip() 
            for q in self.qualifications_text.get("1.0", tk.END).strip().split("\n")
            if q.strip()
        ]

        # Get department ID from selected department name
        department_name = self.department_var.get().strip()
        if not department_name:
            messagebox.showerror("Error", "Department is required")
            return
            
        department_id = self.departments.get(department_name)
        if not department_id:
            messagebox.showerror("Error", "Invalid department selected")
            return

        doctor_data = {
            "name": self.name_var.get().strip(),
            "department_id": department_id,
            "contact_number": self.contact_var.get().strip(),
            "email": self.email_var.get().strip(),
            "specialization": self.specialization_var.get().strip(),
            "qualifications": qualifications,
            "consultation_fee": fee
        }

        try:
            if hasattr(self.controller, "current_doctor_id"):
                # Update existing doctor
                doctor_data["doctor_id"] = self.controller.current_doctor_id
                success = self.doctor_service.update_doctor(doctor_data)
                if success:
                    messagebox.showinfo("Success", "Doctor updated successfully")
                    self.controller.show_frame("DoctorList")
                else:
                    messagebox.showerror("Error", "Failed to update doctor record")
            else:
                # Create new doctor
                doctor = self.doctor_service.create_doctor(**doctor_data)
                if doctor:
                    messagebox.showinfo("Success", "Doctor created successfully")
                    self.controller.current_doctor_id = doctor.doctor_id
                    self.controller.show_frame("DoctorList")
                else:
                    messagebox.showerror("Error", "Failed to create doctor record")

        except mysql.connector.Error as e:
            if e.errno == 1062:  # Duplicate entry error
                messagebox.showerror("Error", "A doctor with this staff ID already exists")
            else:
                messagebox.showerror("Database Error", f"Database operation failed: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
