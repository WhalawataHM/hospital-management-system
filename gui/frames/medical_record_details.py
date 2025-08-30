import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ..base_frame import BaseFrame
from ...services import MedicalRecordService, PatientService, DoctorService
from ..dialogs.patient_search_dialog import PatientSearchDialog
from ..dialogs.doctor_search_dialog import DoctorSearchDialog
from ..dialogs.medical_record_dialogs import PrescriptionDialog, TestResultDialog

class MedicalRecordDetailsFrame(BaseFrame):
    def __init__(self, parent, controller):
        self.medical_record_service = MedicalRecordService()
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
            command=lambda: self.controller.show_frame("MedicalRecordList")
        )
        back_btn.pack(side="left")

        self.title_label = ttk.Label(
            header_frame,
            text="New Medical Record",
            style="Header.TLabel"
        )
        self.title_label.pack(side="left", padx=20)

        # Save button
        self.save_btn = ttk.Button(
            header_frame,
            text="Save",
            command=self.save_record
        )
        self.save_btn.pack(side="right")

        # Create notebook for tabs
        notebook = ttk.Notebook(content)
        notebook.pack(fill="both", expand=True, pady=10)

        # Basic Information tab
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="Basic Information")
        self._create_basic_info_frame(basic_frame)

        # Diagnosis and Treatment tab
        treatment_frame = ttk.Frame(notebook)
        notebook.add(treatment_frame, text="Diagnosis & Treatment")
        self._create_treatment_frame(treatment_frame)

        # Test Results tab
        tests_frame = ttk.Frame(notebook)
        notebook.add(tests_frame, text="Test Results")
        self._create_tests_frame(tests_frame)

    def _create_basic_info_frame(self, parent):
        # Configure grid
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(3, weight=1)

        current_row = 0

        # Patient Selection
        ttk.Label(parent, text="Patient:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        patient_frame = ttk.Frame(parent)
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
        ttk.Label(parent, text="Doctor:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        doctor_frame = ttk.Frame(parent)
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

        # Visit Date
        ttk.Label(parent, text="Visit Date:").grid(row=current_row, column=0, padx=5, pady=5, sticky="e")
        self.visit_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(parent, textvariable=self.visit_date_var, state="readonly")
        date_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")

    def _create_treatment_frame(self, parent):
        # Diagnosis
        diagnosis_frame = ttk.LabelFrame(parent, text="Diagnosis")
        diagnosis_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.diagnosis_text = tk.Text(diagnosis_frame, height=5)
        self.diagnosis_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Prescriptions
        prescriptions_frame = ttk.LabelFrame(parent, text="Prescriptions")
        prescriptions_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Prescription list
        self.prescriptions_list = tk.Listbox(prescriptions_frame, height=5)
        self.prescriptions_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Prescription buttons
        btn_frame = ttk.Frame(prescriptions_frame)
        btn_frame.pack(side="left", fill="y", padx=5, pady=5)

        ttk.Button(
            btn_frame,
            text="Add",
            command=self.add_prescription
        ).pack(fill="x", pady=2)

        ttk.Button(
            btn_frame,
            text="Remove",
            command=self.remove_prescription
        ).pack(fill="x", pady=2)

        # Notes
        notes_frame = ttk.LabelFrame(parent, text="Notes")
        notes_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.notes_text = tk.Text(notes_frame, height=3)
        self.notes_text.pack(fill="both", expand=True, padx=5, pady=5)

    def _create_tests_frame(self, parent):
        # Test Results list
        self.tests_table = self.create_table(
            parent,
            {
                "test_name": 150,
                "test_date": 100,
                "result": 200,
                "notes": 200
            }
        )

        # Buttons frame
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            btn_frame,
            text="Add Test Result",
            command=self.add_test_result
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Remove Test Result",
            command=self.remove_test_result
        ).pack(side="left", padx=5)

    def select_patient(self):
        dialog = PatientSearchDialog(self)
        if dialog.result:
            patient = self.patient_service.get_patient_by_id(dialog.result)
            if patient:
                self.patient_id_var.set(patient.patient_id)
                self.patient_name_var.set(patient.name)

    def select_doctor(self):
        dialog = DoctorSearchDialog(self)
        if dialog.result:
            doctor = self.doctor_service.get_doctor_by_id(dialog.result)
            if doctor:
                self.doctor_id_var.set(doctor.doctor_id)
                self.doctor_name_var.set(doctor.name)

    def add_prescription(self):
        dialog = PrescriptionDialog(self)
        if dialog.result:
            self.prescriptions_list.insert(tk.END, dialog.result)

    def remove_prescription(self):
        selection = self.prescriptions_list.curselection()
        if selection:
            self.prescriptions_list.delete(selection)

    def add_test_result(self):
        dialog = TestResultDialog(self)
        if dialog.result:
            self.tests_table.insert("", "end", values=dialog.result)

    def remove_test_result(self):
        selected_item = self.tests_table.selection()
        if selected_item:
            self.tests_table.delete(selected_item)

    def on_show(self):
        if hasattr(self.controller, "current_record_id"):
            self.load_record(self.controller.current_record_id)
        else:
            self.clear_form()

    def load_record(self, record_id):
        record = self.medical_record_service.get_record_by_id(record_id)
        if record:
            self.title_label.config(text=f"Medical Record: {record.record_id}")
            
            # Set patient
            self.patient_id_var.set(record.patient_id)
            self.patient_name_var.set(record.patient_name)
            
            # Set doctor
            self.doctor_id_var.set(record.doctor_id)
            self.doctor_name_var.set(record.doctor_name)
            
            # Set date
            self.visit_date_var.set(record.visit_date.strftime("%Y-%m-%d"))
            
            # Set diagnosis
            self.diagnosis_text.delete("1.0", tk.END)
            self.diagnosis_text.insert("1.0", record.diagnosis)
            
            # Set prescriptions
            self.prescriptions_list.delete(0, tk.END)
            for prescription in record.prescriptions:
                self.prescriptions_list.insert(tk.END, prescription)
            
            # Set notes
            self.notes_text.delete("1.0", tk.END)
            if record.notes:
                self.notes_text.insert("1.0", record.notes)
            
            # Set test results
            self.tests_table.delete(*self.tests_table.get_children())
            for test in record.test_results:
                self.tests_table.insert("", "end", values=(
                    test["test_name"],
                    test["test_date"],
                    test["result"],
                    test.get("notes", "")
                ))

    def clear_form(self):
        self.title_label.config(text="New Medical Record")
        self.patient_id_var.set("")
        self.patient_name_var.set("")
        self.doctor_id_var.set("")
        self.doctor_name_var.set("")
        self.visit_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.diagnosis_text.delete("1.0", tk.END)
        self.prescriptions_list.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)
        self.tests_table.delete(*self.tests_table.get_children())

    def save_record(self):
        # Validate required fields
        if not self.patient_id_var.get():
            messagebox.showerror("Error", "Please select a patient")
            return

        if not self.doctor_id_var.get():
            messagebox.showerror("Error", "Please select a doctor")
            return

        if not self.diagnosis_text.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "Diagnosis is required")
            return

        record_data = {
            "patient_id": self.patient_id_var.get(),
            "doctor_id": self.doctor_id_var.get(),
            "visit_date": datetime.strptime(self.visit_date_var.get(), "%Y-%m-%d").date(),
            "diagnosis": self.diagnosis_text.get("1.0", tk.END).strip(),
            "prescriptions": list(self.prescriptions_list.get(0, tk.END)),
            "notes": self.notes_text.get("1.0", tk.END).strip(),
            "test_results": [
                {
                    "test_name": self.tests_table.item(item)["values"][0],
                    "test_date": self.tests_table.item(item)["values"][1],
                    "result": self.tests_table.item(item)["values"][2],
                    "notes": self.tests_table.item(item)["values"][3]
                }
                for item in self.tests_table.get_children()
            ]
        }

        try:
            if hasattr(self.controller, "current_record_id"):
                # Update existing record
                record_data["record_id"] = self.controller.current_record_id
                success = self.medical_record_service.update_record(record_data)
                if success:
                    messagebox.showinfo("Success", "Medical record updated successfully")
            else:
                # Create new record
                record = self.medical_record_service.create_record(**record_data)
                if record:
                    messagebox.showinfo("Success", "Medical record created successfully")

            # Return to record list
            self.controller.show_frame("MedicalRecordList")

        except Exception as e:
            messagebox.showerror("Error", str(e))

class PrescriptionDialog:
    def __init__(self, parent):
        self.result = None
        # Implement prescription dialog
        pass

class TestResultDialog:
    def __init__(self, parent):
        self.result = None
        # Implement test result dialog
        pass
