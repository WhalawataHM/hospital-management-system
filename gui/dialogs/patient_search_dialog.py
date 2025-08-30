import tkinter as tk
from tkinter import ttk
from datetime import date
from ...services import PatientService

class PatientSearchDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.patient_service = PatientService()
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Select Patient")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog modal
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.create_widgets()
        self.dialog.wait_window()
    
    def create_widgets(self):
        # Search frame
        search_frame = ttk.Frame(self.dialog, padding="5")
        search_frame.pack(fill="x", padx=5, pady=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Results table
        columns = {
            "id": 80,
            "name": 200,
            "contact": 150,
            "age": 50
        }
        
        self.table = ttk.Treeview(
            self.dialog,
            columns=list(columns.keys()),
            show="headings",
            height=10
        )
        
        # Configure columns
        for col, width in columns.items():
            self.table.heading(col, text=col.title())
            self.table.column(col, width=width)
        
        self.table.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.dialog, padding="5")
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Select", command=self.on_select).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.on_close).pack(side="left")
        
        # Double click to select
        self.table.bind("<Double-1>", lambda e: self.on_select())
        
        # Load initial data
        self.load_patients()
    
    def load_patients(self, search_term=None):
        # Clear current items
        for item in self.table.get_children():
            self.table.delete(item)
            
        # Get patients from service
        patients = self.patient_service.search_patients(search_term) if search_term else self.patient_service.get_all_patients()
        
        # Add to table
        for patient in patients:
            self.table.insert("", "end", values=(
                patient.patient_id,
                patient.name,
                patient.contact_number,
                # Calculate age from date_of_birth
                (date.today().year - patient.date_of_birth.year) 
                    if hasattr(patient, 'date_of_birth') else ''
            ))
    
    def on_search_change(self, *args):
        self.load_patients(self.search_var.get())
    
    def on_select(self):
        selected_item = self.table.selection()
        if selected_item:
            values = self.table.item(selected_item)["values"]
            self.result = values[0]  # Get ID
            self.dialog.destroy()
    
    def on_close(self):
        self.dialog.destroy()
