import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from ..base_frame import BaseFrame
from ...services import AppointmentService, PatientService, DoctorService

class AppointmentDetailsFrame(BaseFrame):
    def __init__(self, parent, controller):
        self.appointment_service = AppointmentService()
        self.patient_service = PatientService()
        self.doctor_service = DoctorService()
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
            command=lambda: self.controller.show_frame("AppointmentList")
        )
        back_btn.pack(side="left")

        self.title_label = ttk.Label(
            header_frame,
            text="Schedule New Appointment",
            style="Header.TLabel"
        )
        self.title_label.pack(side="left", padx=20)

        # Save button
        self.save_btn = ttk.Button(
            header_frame,
            text="Save",
            command=self.save_appointment
        )
        self.save_btn.pack(side="right")

        # Create form
        form_frame = ttk.LabelFrame(content, text="Appointment Information")
        form_frame.pack(fill="x", pady=10)

        # Configure grid
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        current_row = 0

        # Patient Selection
        ttk.Label(form_frame, text="Patient:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        patient_frame = ttk.Frame(form_frame)
        patient_frame.grid(row=current_row, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

        self.patient_id_var = tk.StringVar()
        self.patient_name_var = tk.StringVar()
        
        patient_entry = ttk.Entry(
            patient_frame,
            textvariable=self.patient_name_var,
            state="readonly"
        )
        patient_entry.pack(side="left", fill="x", expand=True)

        ttk.Button(
            patient_frame,
            text="Select Patient",
            command=self.select_patient
        ).pack(side="left", padx=5)

        current_row += 1

        # Doctor Selection
        ttk.Label(form_frame, text="Doctor:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        doctor_frame = ttk.Frame(form_frame)
        doctor_frame.grid(row=current_row, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

        self.doctor_id_var = tk.StringVar()
        self.doctor_name_var = tk.StringVar()
        
        doctor_entry = ttk.Entry(
            doctor_frame,
            textvariable=self.doctor_name_var,
            state="readonly"
        )
        doctor_entry.pack(side="left", fill="x", expand=True)

        ttk.Button(
            doctor_frame,
            text="Select Doctor",
            command=self.select_doctor
        ).pack(side="left", padx=5)

        current_row += 1

        # Date and Time
        ttk.Label(form_frame, text="Date:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = DateEntry(
            form_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            mindate=datetime.now()
        )
        self.date_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="w")
        self.date_entry.bind("<<DateEntrySelected>>", self.on_date_change)

        ttk.Label(form_frame, text="Time:").grid(row=current_row, column=2, padx=5, pady=5, sticky="e")
        self.time_var = tk.StringVar()
        self.time_combo = ttk.Combobox(
            form_frame,
            textvariable=self.time_var,
            state="readonly",
            width=10
        )
        self.time_combo.grid(row=current_row, column=3, padx=5, pady=5, sticky="w")

        current_row += 1

        # Department
        ttk.Label(form_frame, text="Department:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.department_var = tk.StringVar()
        self.department_entry = ttk.Entry(
            form_frame,
            textvariable=self.department_var,
            state="readonly"
        )
        self.department_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")

        # Status
        ttk.Label(form_frame, text="Status:").grid(row=current_row, column=2, padx=5, pady=5, sticky="e")
        self.status_var = tk.StringVar(value="Scheduled")
        status_combo = ttk.Combobox(
            form_frame,
            textvariable=self.status_var,
            values=["Scheduled", "Completed", "Cancelled", "No Show"],
            state="readonly"
        )
        status_combo.grid(row=current_row, column=3, padx=5, pady=5, sticky="ew")

        current_row += 1

        # Notes
        ttk.Label(form_frame, text="Notes:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.notes_text = tk.Text(form_frame, height=3, width=40)
        self.notes_text.grid(row=current_row, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Initialize time slots
        self.update_time_slots()

    def update_time_slots(self):
        times = []
        start = datetime.strptime("09:00", "%H:%M")
        end = datetime.strptime("17:00", "%H:%M")
        slot = timedelta(minutes=30)

        current = start
        while current <= end:
            times.append(current.strftime("%H:%M"))
            current += slot

        self.time_combo['values'] = times
        if not self.time_var.get():
            self.time_var.set(times[0])

    def on_date_change(self, event=None):
        if self.doctor_id_var.get():
            self.update_available_slots()

    def update_available_slots(self):
        selected_date = self.date_entry.get_date()
        doctor_id = self.doctor_id_var.get()
        
        # Get booked slots
        booked_slots = self.appointment_service.get_doctor_booked_slots(
            doctor_id,
            selected_date
        )
        
        # Update available times
        all_slots = self.time_combo['values']
        available_slots = [slot for slot in all_slots if slot not in booked_slots]
        
        self.time_combo['values'] = available_slots
        if available_slots:
            self.time_var.set(available_slots[0])
        else:
            self.time_var.set('')

    def select_patient(self):
        # This would typically open a patient search dialog
        # For now, we'll use a simple dialog
        dialog = PatientSearchDialog(self)
        if dialog.result:
            patient = self.patient_service.get_patient_by_id(dialog.result)
            if patient:
                self.patient_id_var.set(patient.patient_id)
                self.patient_name_var.set(patient.name)

    def select_doctor(self):
        # This would typically open a doctor search dialog
        # For now, we'll use a simple dialog
        dialog = DoctorSearchDialog(self)
        if dialog.result:
            doctor = self.doctor_service.get_doctor_by_id(dialog.result)
            if doctor:
                self.doctor_id_var.set(doctor.doctor_id)
                self.doctor_name_var.set(doctor.name)
                self.department_var.set(doctor.specialization)
                self.update_available_slots()

    def on_show(self):
        if hasattr(self.controller, "current_appointment_id"):
            self.load_appointment(self.controller.current_appointment_id)
        else:
            self.clear_form()

    def load_appointment(self, appointment_id):
        appointment = self.appointment_service.get_appointment_by_id(appointment_id)
        if appointment:
            self.title_label.config(text=f"Appointment: {appointment.appointment_id}")
            
            # Set patient
            self.patient_id_var.set(appointment.patient_id)
            self.patient_name_var.set(appointment.patient_name)
            
            # Set doctor
            self.doctor_id_var.set(appointment.doctor_id)
            self.doctor_name_var.set(appointment.doctor_name)
            
            # Set date and time
            self.date_entry.set_date(appointment.date_time.date())
            self.time_var.set(appointment.date_time.strftime("%H:%M"))
            
            # Set other fields
            self.department_var.set(appointment.department)
            self.status_var.set(appointment.status)
            self.notes_text.delete("1.0", tk.END)
            if appointment.notes:
                self.notes_text.insert("1.0", appointment.notes)

    def clear_form(self):
        self.title_label.config(text="Schedule New Appointment")
        self.patient_id_var.set("")
        self.patient_name_var.set("")
        self.doctor_id_var.set("")
        self.doctor_name_var.set("")
        self.date_entry.set_date(datetime.now())
        self.time_var.set("")
        self.department_var.set("")
        self.status_var.set("Scheduled")
        self.notes_text.delete("1.0", tk.END)
        self.update_time_slots()

    def save_appointment(self):
        # Validate required fields
        if not self.patient_id_var.get():
            messagebox.showerror("Error", "Please select a patient")
            return

        if not self.doctor_id_var.get():
            messagebox.showerror("Error", "Please select a doctor")
            return

        # Create appointment date_time
        try:
            date = self.date_entry.get_date()
            time = datetime.strptime(self.time_var.get(), "%H:%M").time()
            date_time = datetime.combine(date, time)
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time")
            return

        appointment_data = {
            "patient_id": self.patient_id_var.get(),
            "doctor_id": self.doctor_id_var.get(),
            "date_time": date_time,
            "department": self.department_var.get(),
            "status": self.status_var.get(),
            "notes": self.notes_text.get("1.0", tk.END).strip()
        }

        try:
            if hasattr(self.controller, "current_appointment_id"):
                # Update existing appointment
                appointment_data["appointment_id"] = self.controller.current_appointment_id
                success = self.appointment_service.update_appointment(appointment_data)
                if success:
                    messagebox.showinfo("Success", "Appointment updated successfully")
            else:
                # Create new appointment
                appointment = self.appointment_service.create_appointment(**appointment_data)
                if appointment:
                    messagebox.showinfo("Success", "Appointment scheduled successfully")

            # Return to appointment list
            self.controller.show_frame("AppointmentList")

        except Exception as e:
            messagebox.showerror("Error", str(e))

class PatientSearchDialog:
    def __init__(self, parent):
        self.result = None
        # Implement patient search dialog
        pass

class DoctorSearchDialog:
    def __init__(self, parent):
        self.result = None
        # Implement doctor search dialog
        pass
