import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from ..base_frame import BaseFrame
from ...services import MedicalRecordService

class MedicalRecordListFrame(BaseFrame):
    def __init__(self, parent, controller):
        self.medical_record_service = MedicalRecordService()
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
            text="Medical Records",
            style="Header.TLabel"
        )
        title.pack(side="left")

        # Add Record button
        add_btn = ttk.Button(
            header_frame,
            text="Add Medical Record",
            command=self.add_record
        )
        add_btn.pack(side="right")

        # Filter frame
        filter_frame = ttk.Frame(content)
        filter_frame.pack(fill="x", pady=(0, 20))

        # Patient search
        ttk.Label(filter_frame, text="Patient:").pack(side="left", padx=5)
        self.patient_search_var = tk.StringVar()
        self.patient_search_var.trace("w", self.on_search_change)
        patient_search = ttk.Entry(filter_frame, textvariable=self.patient_search_var)
        patient_search.pack(side="left", padx=5)

        # Doctor search
        ttk.Label(filter_frame, text="Doctor:").pack(side="left", padx=5)
        self.doctor_search_var = tk.StringVar()
        self.doctor_search_var.trace("w", self.on_search_change)
        doctor_search = ttk.Entry(filter_frame, textvariable=self.doctor_search_var)
        doctor_search.pack(side="left", padx=5)

        # Date range
        ttk.Label(filter_frame, text="Date Range:").pack(side="left", padx=5)
        self.date_var = tk.StringVar(value="All")
        date_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.date_var,
            values=["All", "Today", "This Week", "This Month", "This Year"],
            width=15
        )
        date_combo.pack(side="left", padx=5)
        date_combo.bind('<<ComboboxSelected>>', self.on_filter_change)

        # Create table
        self.table = self.create_table(
            content,
            {
                "id": 100,
                "date": 100,
                "patient": 150,
                "doctor": 150,
                "diagnosis": 200,
                "prescriptions": 200,
                "tests": 150
            },
            height=15
        )

        # Bind double click event
        self.table.bind("<Double-1>", self.on_record_select)

        # Add right-click menu
        self.create_context_menu()

    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="View Details", command=self.view_details)
        self.context_menu.add_command(label="Add Test Results", command=self.add_test_results)
        self.context_menu.add_command(label="Print Record", command=self.print_record)

        # Bind right-click event
        self.table.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        try:
            selected_item = self.table.selection()[0]
            self.table.selection_set(selected_item)
            self.context_menu.post(event.x_root, event.y_root)
        except IndexError:
            pass

    def on_show(self):
        self.load_records()

    def load_records(self):
        # Clear existing items
        self.table.delete(*self.table.get_children())

        # Get medical records based on filters
        records = self.filter_records()

        for record in records:
            self.table.insert(
                "",
                "end",
                values=(
                    record.record_id,
                    record.visit_date.strftime("%Y-%m-%d"),
                    record.patient_name,
                    record.doctor_name,
                    record.diagnosis[:50] + "..." if len(record.diagnosis) > 50 else record.diagnosis,
                    ", ".join(record.prescriptions[:3]) + "..." if len(record.prescriptions) > 3 else ", ".join(record.prescriptions),
                    f"{len(record.test_results)} tests" if record.test_results else "No tests"
                )
            )

    def filter_records(self):
        patient_search = self.patient_search_var.get().strip()
        doctor_search = self.doctor_search_var.get().strip()
        date_range = self.date_var.get()

        # Get date range based on filter
        start_date, end_date = self.get_date_range(date_range)

        return self.medical_record_service.search_records(
            patient_search=patient_search,
            doctor_search=doctor_search,
            start_date=start_date,
            end_date=end_date
        )

    def get_date_range(self, date_range):
        today = datetime.now().date()
        if date_range == "Today":
            return today, today
        elif date_range == "This Week":
            week_start = today - timedelta(days=today.weekday())
            return week_start, today
        elif date_range == "This Month":
            month_start = today.replace(day=1)
            return month_start, today
        elif date_range == "This Year":
            year_start = today.replace(month=1, day=1)
            return year_start, today
        return None, None  # All dates

    def on_search_change(self, *args):
        self.load_records()

    def on_filter_change(self, event=None):
        self.load_records()

    def add_record(self):
        if hasattr(self.controller, "current_record_id"):
            delattr(self.controller, "current_record_id")
        self.controller.show_frame("MedicalRecordDetails")

    def on_record_select(self, event):
        selected_item = self.table.selection()
        if not selected_item:
            return

        record_id = self.table.item(selected_item[0])["values"][0]
        self.controller.current_record_id = record_id
        self.view_details()

    def view_details(self):
        if hasattr(self.controller, "current_record_id"):
            self.controller.show_frame("MedicalRecordDetails")

    def add_test_results(self):
        selected_item = self.table.selection()
        if not selected_item:
            return

        record_id = self.table.item(selected_item[0])["values"][0]
        # Open test results dialog
        dialog = TestResultsDialog(self, record_id)
        if dialog.result:
            self.load_records()

    def print_record(self):
        selected_item = self.table.selection()
        if not selected_item:
            return

        record_id = self.table.item(selected_item[0])["values"][0]
        try:
            # Generate PDF report
            success = self.medical_record_service.generate_report(record_id)
            if success:
                messagebox.showinfo("Success", "Medical record report generated successfully")
            else:
                messagebox.showerror("Error", "Failed to generate report")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class TestResultsDialog:
    def __init__(self, parent, record_id):
        self.result = None
        # Implement test results dialog
        pass
