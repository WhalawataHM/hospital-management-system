import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from ..base_frame import BaseFrame
from ...services import AppointmentService

class AppointmentListFrame(BaseFrame):
    def __init__(self, parent, controller):
        self.appointment_service = AppointmentService()
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
            text="Appointments",
            style="Header.TLabel"
        )
        title.pack(side="left")

        # Add Appointment button
        add_btn = ttk.Button(
            header_frame,
            text="Schedule Appointment",
            command=self.schedule_appointment
        )
        add_btn.pack(side="right")

        # Filter frame
        filter_frame = ttk.Frame(content)
        filter_frame.pack(fill="x", pady=(0, 20))

        # Date range filter
        ttk.Label(filter_frame, text="Date Range:").pack(side="left", padx=5)
        self.date_var = tk.StringVar(value="Today")
        date_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.date_var,
            values=["Today", "Tomorrow", "This Week", "This Month", "All"],
            width=15
        )
        date_combo.pack(side="left", padx=5)
        date_combo.bind('<<ComboboxSelected>>', self.on_filter_change)

        # Status filter
        ttk.Label(filter_frame, text="Status:").pack(side="left", padx=5)
        self.status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=["All", "Scheduled", "Completed", "Cancelled", "No Show"],
            width=15
        )
        status_combo.pack(side="left", padx=5)
        status_combo.bind('<<ComboboxSelected>>', self.on_filter_change)

        # Search
        ttk.Label(filter_frame, text="Search:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Create table
        self.table = self.create_table(
            content,
            {
                "id": 100,
                "date": 100,
                "time": 80,
                "patient": 150,
                "doctor": 150,
                "department": 120,
                "status": 100,
                "notes": 200
            },
            height=15
        )

        # Bind double click event
        self.table.bind("<Double-1>", self.on_appointment_select)

        # Add right-click menu
        self.create_context_menu()

    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="View Details", command=self.view_details)
        self.context_menu.add_command(label="Mark Complete", command=lambda: self.update_status("Completed"))
        self.context_menu.add_command(label="Mark No Show", command=lambda: self.update_status("No Show"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Cancel Appointment", command=self.cancel_appointment)

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
        self.load_appointments()

    def load_appointments(self):
        # Clear existing items
        self.table.delete(*self.table.get_children())

        # Get date range based on filter
        start_date, end_date = self.get_date_range()

        # Get appointments based on filters
        appointments = self.filter_appointments(start_date, end_date)

        for apt in appointments:
            self.table.insert(
                "",
                "end",
                values=(
                    apt.appointment_id,
                    apt.date_time.strftime("%Y-%m-%d"),
                    apt.date_time.strftime("%H:%M"),
                    apt.patient_name,
                    apt.doctor_name,
                    apt.department,
                    apt.status,
                    apt.notes or ""
                )
            )

    def get_date_range(self):
        today = datetime.now().date()
        if self.date_var.get() == "Today":
            return today, today
        elif self.date_var.get() == "Tomorrow":
            tomorrow = today + timedelta(days=1)
            return tomorrow, tomorrow
        elif self.date_var.get() == "This Week":
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            return week_start, week_end
        elif self.date_var.get() == "This Month":
            month_start = today.replace(day=1)
            if today.month == 12:
                next_month = today.replace(year=today.year + 1, month=1, day=1)
            else:
                next_month = today.replace(month=today.month + 1, day=1)
            month_end = next_month - timedelta(days=1)
            return month_start, month_end
        else:  # All
            return None, None

    def filter_appointments(self, start_date, end_date):
        appointments = self.appointment_service.get_appointments(
            start_date=start_date,
            end_date=end_date,
            status=None if self.status_var.get() == "All" else self.status_var.get(),
            search_term=self.search_var.get().strip()
        )
        return appointments

    def on_filter_change(self, event=None):
        self.load_appointments()

    def on_search_change(self, *args):
        self.load_appointments()

    def schedule_appointment(self):
        # Clear current appointment selection
        if hasattr(self.controller, "current_appointment_id"):
            delattr(self.controller, "current_appointment_id")
        self.controller.show_frame("AppointmentDetails")

    def on_appointment_select(self, event):
        selected_item = self.table.selection()
        if not selected_item:
            return

        appointment_id = self.table.item(selected_item[0])["values"][0]
        self.controller.current_appointment_id = appointment_id
        self.view_details()

    def view_details(self):
        if hasattr(self.controller, "current_appointment_id"):
            self.controller.show_frame("AppointmentDetails")

    def update_status(self, status):
        selected_item = self.table.selection()
        if not selected_item:
            return

        appointment_id = self.table.item(selected_item[0])["values"][0]
        try:
            if self.appointment_service.update_appointment_status(appointment_id, status):
                messagebox.showinfo("Success", f"Appointment marked as {status}")
                self.load_appointments()
            else:
                messagebox.showerror("Error", "Failed to update appointment status")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_appointment(self):
        selected_item = self.table.selection()
        if not selected_item:
            return

        appointment_id = self.table.item(selected_item[0])["values"][0]
        if messagebox.askyesno("Confirm Cancellation", 
                             "Are you sure you want to cancel this appointment?"):
            try:
                if self.appointment_service.cancel_appointment(appointment_id):
                    messagebox.showinfo("Success", "Appointment cancelled successfully")
                    self.load_appointments()
                else:
                    messagebox.showerror("Error", "Failed to cancel appointment")
            except Exception as e:
                messagebox.showerror("Error", str(e))
