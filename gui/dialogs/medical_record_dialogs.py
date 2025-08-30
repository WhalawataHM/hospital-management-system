import tkinter as tk
from tkinter import ttk
from datetime import datetime

class PrescriptionDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Prescription")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog modal
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.create_widgets()
        self.dialog.wait_window()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Medication name
        ttk.Label(main_frame, text="Medication:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.med_name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.med_name_var).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Dosage
        ttk.Label(main_frame, text="Dosage:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.dosage_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.dosage_var).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Frequency
        ttk.Label(main_frame, text="Frequency:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.frequency_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.frequency_var).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        # Duration
        ttk.Label(main_frame, text="Duration:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.duration_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.duration_var).grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        # Notes
        ttk.Label(main_frame, text="Notes:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.notes_text = tk.Text(main_frame, height=3, width=30)
        self.notes_text.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self.on_save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.on_close).pack(side="left")
    
    def validate_fields(self):
        if not self.med_name_var.get().strip():
            return "Medication name is required"
        if not self.dosage_var.get().strip():
            return "Dosage is required"
        if not self.frequency_var.get().strip():
            return "Frequency is required"
        return None
    
    def on_save(self):
        error = self.validate_fields()
        if error:
            tk.messagebox.showerror("Error", error)
            return
        
        # Format prescription string
        prescription = (
            f"{self.med_name_var.get().strip()} - "
            f"{self.dosage_var.get().strip()}, "
            f"{self.frequency_var.get().strip()}"
        )
        
        if self.duration_var.get().strip():
            prescription += f" for {self.duration_var.get().strip()}"
            
        notes = self.notes_text.get("1.0", tk.END).strip()
        if notes:
            prescription += f" (Notes: {notes})"
        
        self.result = prescription
        self.dialog.destroy()
    
    def on_close(self):
        self.dialog.destroy()

class TestResultDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Test Result")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog modal
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.create_widgets()
        self.dialog.wait_window()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Test name
        ttk.Label(main_frame, text="Test Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.test_name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.test_name_var).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Test date
        ttk.Label(main_frame, text="Test Date:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.test_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(main_frame, textvariable=self.test_date_var).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Result
        ttk.Label(main_frame, text="Result:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.result_text = tk.Text(main_frame, height=3, width=30)
        self.result_text.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        # Notes
        ttk.Label(main_frame, text="Notes:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.notes_text = tk.Text(main_frame, height=3, width=30)
        self.notes_text.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self.on_save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.on_close).pack(side="left")
    
    def validate_fields(self):
        if not self.test_name_var.get().strip():
            return "Test name is required"
        if not self.test_date_var.get().strip():
            return "Test date is required"
        if not self.result_text.get("1.0", tk.END).strip():
            return "Result is required"
        try:
            datetime.strptime(self.test_date_var.get(), "%Y-%m-%d")
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD"
        return None
    
    def on_save(self):
        error = self.validate_fields()
        if error:
            tk.messagebox.showerror("Error", error)
            return
        
        self.result = (
            self.test_name_var.get().strip(),
            self.test_date_var.get().strip(),
            self.result_text.get("1.0", tk.END).strip(),
            self.notes_text.get("1.0", tk.END).strip()
        )
        self.dialog.destroy()
    
    def on_close(self):
        self.dialog.destroy()
